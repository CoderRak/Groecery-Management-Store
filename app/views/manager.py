from flask import render_template, current_app as app, request, redirect, url_for,make_response,session
from ..controller import createManager,getManager,createCategory,deleteCategory,editCategory,getCategory,createItem,editItem,getItem,deleteItem,getItemByName,changePriceofItem,deleteCartItemByItemId
from ..utils import custom_decrypt, validToken, detokenize,db
from .auth import authorizeUser
from datetime import datetime
from ..models import Category,Item
import matplotlib.pyplot as plt
import base64
import matplotlib
matplotlib.use('Agg')

def isManager(token):
    return (validToken(token) and detokenize(token)['role'] == 'manager')


@app.route('/manager/login',methods=['GET','POST'])
def manager_login():
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if validToken(auth):
            return redirect(url_for('manager_home'))   
        else:
            return redirect(url_for('logout'))

    
    def getLogin():
        return render_template('manager_login.html', isManager=True, isAuth=True)
    
    def postLogin():
        d = request.form
        user = getManager(email=d['email'])  
        if (user):
            if custom_decrypt(string=user.password) == d['password']:
                session['email']=d['email']
                return authorizeUser(user=user, action=lambda:redirect(url_for('manager_home')), role='manager')
            else:
                return render_template('manager_login.html', isManager=True, isAuth=True, error='Wrong password')
        else:
            return render_template('manager_login.html', isManager=True, isAuth=True, error='No Manager found with these credentials')

    return {
        'GET': getLogin,
        'POST': postLogin,
    }[m]()

@app.route('/manager/register',methods=['GET','POST'])
def manager_register():
    
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if validToken(auth):
            return redirect(url_for('manager_home'))
        else:
            return redirect(url_for('logout'))   
    
    def getSignup():
        return render_template('manager_register.html', isManager=True, isAuth=True)
    def postSignup():
        d = request.form
        data = {
            'name': d['name'],
            'email': d['email'],
            'password': d['password']
        }
        user = createManager(data)
        if (user):
            return authorizeUser(user=user, action=lambda:redirect(url_for('manager_home')), role='manager')
        else:
            return render_template('manager_register.html', isManager=True, isAuth=True, error='Something went wrong')

    return {
        'GET': getSignup,
        'POST': postSignup,
    }[m]()


@app.route('/manager/home',methods=['GET'])
def manager_home():
    
    success_message = request.args.get('success_message')
    email=session['email']
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isManager(auth):
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('manager_login'))
    
    categories = db.session.query(Category).all()
    items = db.session.query(Item).all()
    d = {}
    
    manager=getManager(email=email)
    for category in categories:
        d[category.cid] = []
    for item in items:
        d[item.category_id].append(item)
    if request.method=='GET':
        return render_template('manager_home.html', isManager=True,isAuth=False,d=d,categories=categories,items=items,manager=manager,success_message=success_message)
    
@app.route('/manager/summary', methods=['GET', 'POST'])
def manager_summary():
    items = db.session.query(Item).all()
    categories = db.session.query(Category).all()
    a = []
    b = []
    c = []
    d = []
    for item in items:
        a.append(item.name)
        temp = float(item.qty)-float(item.qty_left)
        b.append(temp)





    for category in categories:
        c.append(category.cname)
        s = 0
        for item in items:
            if category.cid == item.category_id:
                s += float(item.qty)-float(item.qty_left)
        d.append(s)
    plt.bar(a, b)
    plt.xlabel('Items')
    plt.ylabel('Quantity Bought Last Week')
    plt.title('Items vs Quantity Bought Last week')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    plt.savefig('a_vs_b.png')
    

    plt.figure()
    plt.bar(c, d)
    plt.xlabel('Categories')
    plt.ylabel('Total Quantity Bought Last week')
    plt.title('Categories vs Total Bought Last week')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    plt.savefig('c_vs_d.png')

    with open('a_vs_b.png', 'rb') as img_file:
        a_vs_b_base64 = base64.b64encode(img_file.read()).decode()
    
    with open('c_vs_d.png', 'rb') as img_file:
        c_vs_d_base64 = base64.b64encode(img_file.read()).decode()

    a_vs_b_html = '<img src="data:image/png;base64,{}" alt="a_vs_b">'.format(a_vs_b_base64)
    c_vs_d_html = '<img src="data:image/png;base64,{}" alt="c_vs_d">'.format(c_vs_d_base64)

    return f'''
    <html>
    <body>
        <h1>Manager Summary</h1>
        <div style="display: flex; flex-direction: row; justify-content: space-between;">
            <div>
                <h2>Items vs Quantity Difference</h2>
                {a_vs_b_html}
            </div>
            <div>
                <h2>Categories vs Total Quantity Difference</h2>
                {c_vs_d_html}
            </div>
        </div>
    </body>
    </html>
'''

    

@app.route('/manager/category/create',methods=['GET','POST'])
def create_category():
    m=request.method

    def getCateg():
        return render_template('create_category.html', isManager=True,isAuth=False,manager=getManager(session['email']))
    

    def postCateg():
        d=request.form
        cate=getCategory(cname=d['name'])
        if(cate):
            return render_template('create_category.html', isManager=True, isAuth=False, manager=getManager(session['email']),error='Category of same name already exists')

        else:
            data = {
            'cname': d['name'],
            }
            new_categ=createCategory(data)
            success_message = "Category created successfully"
            return redirect(url_for('manager_home', success_message=success_message))

    return {
        'GET': getCateg,
        'POST': postCateg,
    }[m]()


@app.route('/manager/edit/category/<cid>',methods=['GET','POST'])
def edit_category(cid):
    m=request.method
    def getEditCateg():
        return render_template('edit_category.html', isManager=True,isAuth=False,manager=getManager(session['email']),cid=cid)

    def postEditCateg():
        d=request.form
        cate=getCategory(cid=cid)
        D={}
        D['cid']=cid
        D['cname']=d['name']
        if(cate):
            new_cate=editCategory(D)
            success_message = "Category edited successfully"
            return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), success_message='Category updated successfully'))
        else:
            return redirect(url_for('manager_home'),isManager=True, isAuth=False, manager=getManager(session['email']),error='Couldnt edit category name,try again please')
            
    return {
        'GET': getEditCateg,
        'POST': postEditCateg,
    }[m]()


@app.route('/manager/delete/category/<cid>',methods=['GET','POST'])
def delete_category(cid):
    categid=cid
    categ=getCategory(cid=cid)
    dele=deleteCategory(categ.cid)
    if(dele):
        return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), success_message='Category deleted successfully'))
    else:
        return redirect(url_for('manager_home'),isManager=True, isAuth=False, manager=getManager(session['email']),error='Couldnt delete category,try again please')
            

@app.route('/manager/create/item/<cid>',methods=['GET','POST'])
def create_item(cid):
    m=request.method
    categ=getCategory(cid=str(cid))
    def getCreateItem():
        return render_template('create_item.html', isManager=True,isAuth=False,manager=getManager(session['email']),cid=categ.cid)
    

    def postCreateItem():
        d=request.form
        cate=getItemByName(name=d['name'])
        
        if(cate):
            return render_template('create_item.html', isManager=True, isAuth=False, manager=getManager(session['email']),error='Item of same name already exists',cid=cid)
        else:
            data = {
            'category_id':cid,
            'name':d['name'],
            'unit':d['unit'],
            'unit_price':d['unit_price'],
            'qty':d['qty'],
            'qty_left':d['qty'],
            'mdate':d['mdate']
            }
            data['mdate'] = datetime.strptime(data['mdate'], '%Y-%m-%d').date()
            new_item=createItem(data)
            success_message = "Item created successfully"
            return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), success_message=success_message))
            
    return {
        'GET': getCreateItem,
        'POST': postCreateItem,
    }[m]()

@app.route('/manager/edit/item/<item_id>',methods=['GET','POST'])
def edit_item(item_id):
    item=getItem(item_id=item_id)
    m=request.method
    

    categ=getCategory(cid=item.category_id)
    def getEditItem():
        return render_template('edit_item.html', isManager=True,isAuth=False,manager=getManager(session['email']),cid=categ.cid,item=item)
    

    def postEditItem():
        d=request.form
        data = {
            'item_id':item.item_id,
            'category_id':item.category_id,
            'name':item.name,
            'unit':d['unit'],
            'unit_price':d['unit_price'],
            'qty':d['qty'],
            'qty_left':d['qty'],
            'mdate':d['mdate']
        }
        data['mdate'] = datetime.strptime(data['mdate'], '%Y-%m-%d').date()
        new_item=editItem(data)
        if(new_item):
            success_message = "Item edited successfully"
            change=changePriceofItem(item_id=item.item_id,unit_price=d['unit_price'])
            if(change):
                return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), success_message=success_message))
            
            else:
                error = "Couldnt Edit item try again"
                return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), error=error))
        else:
            error = "Couldnt Edit item try again"
            return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), error=error))
            
    return {
        'GET': getEditItem,
        'POST': postEditItem,
    }[m]()

@app.route('/manager/delete/item/<item_id>',methods=['GET','POST'])
def delete_item(item_id):
    delCart=deleteCartItemByItemId(item_id=item_id)
    if(delCart):
        deleItem=deleteItem(item_id=item_id)
        if(deleItem):
            success_message="Item deleted successfully"
            return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), success_message=success_message))
        else:
            error="Couldnt delete Item,try again"
            return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), error=error))
    else:
        error="Couldnt delete Item,try again"
        return redirect(url_for('manager_home', isManager=True, isAuth=False, manager=getManager(session['email']), error=error))

@app.route('/logout')
def logout():
    res = make_response(redirect(url_for('manager_login')))
    res.delete_cookie('token')
    return res
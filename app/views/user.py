from flask import render_template, current_app as app, request, redirect, url_for,make_response,session
from ..controller import createUser,editUser,getAllItem,getItem,editItem,getCategory,getAllCategory,createCartItem,editCartItem,getUser,getCartsByUserId,createCart,createCartItem,editCartItem,ListItemsInCart,totalPriceOfCart,deleteCartItem,createPostbuy,getPostBuyItemByUserId
from ..utils import custom_decrypt, validToken, detokenize,db
from .auth import authorizeUser
from ..models import Category,Item,Postbuy
from datetime import datetime
def isUser(token):
    return (validToken(token) and detokenize(token)['role'] == 'user')


@app.route('/',methods=['GET','POST'])
def user_login():
    m=request.method

    auth = request.cookies.get('token', None)
    if auth:
        if validToken(auth):
            return redirect(url_for('user_home'))
        else:
            return redirect(url_for('user_logout'))
    def getLogin():
        return render_template('user_login.html',isUser=True,isAuth=True)
    
    def postLogin():
        d=request.form
        D= {
            'email': d['email'],
            'password': d['password']
        }
        user=getUser(email=D['email'])
        if(user):
            if custom_decrypt(string=user.password) == d['password']:
                session['email']=d['email']
                return authorizeUser(user=user, action=lambda:redirect(url_for('user_home')), role='user')
            else:
                return render_template('user_login.html', isUser=True, isAuth=True, error='Wrong password')
        else:
            return render_template('user_login.html', isUser=True, isAuth=True, error='No User found with these credentials')

    return {
        'GET': getLogin,
        'POST': postLogin,
    }[m]()

@app.route('/register',methods=['GET','POST'])
def user_register():
    m=request.method
    auth=request.cookies.get('token',None)
    if auth:
        if validToken(auth):
            return redirect(url_for('user_home'))
        else:
            return redirect(url_for('logout'))
    def getSignUp():
        return render_template('user_register.html',isUser=True,isAuth=True)
    
    def postSignUp():
        d = request.form
        data = {
            'name': d['name'],
            'email': d['email'],
            'phoneno': d['phoneno'],
            'password': d['password']
        }
        user = createUser(data)
        
        if (user):
            D={'user_id':user.user_id}
            cart=createCart(D)
            return authorizeUser(user=user, action=lambda:redirect(url_for('user_home')), role='user')
        else:
            return render_template('user_register.html', isUser=True, isAuth=True, error='Something went wrong')

    return {
        'GET': getSignUp,
        'POST': postSignUp,
    }[m]()


@app.route('/user/home',methods=['GET','POST'])
def user_home():
    global flag
    flag=0
    m=request.method
    success_message = request.args.get('success_message')
    email=session['email']
    m = request.method
    auth = request.cookies.get('token', None)

    if auth:
        if not isUser(auth):
            return redirect(url_for('user_logout'))
    else:
        return redirect(url_for('user_login'))
    
    categories = db.session.query(Category).all()
    items = db.session.query(Item).all()
    d = {}
    user=getUser(email=email)
    for category in categories:
        d[category.cid] = []

    for item in items:
        d[item.category_id].append(item)

    if request.method=='GET':
        return render_template('user_home.html', isUser=True,isAuth=False,d=d,categories=categories,items=items,user=user,success_message=success_message)
    




@app.route('/user/profile/<user_id>',methods=['GET','POST'])
def user_profile(user_id):
    user=getUser(user_id=user_id)
    items=getPostBuyItemByUserId(user_id=user_id)
    return render_template('user_profile.html', isUser=True,isAuth=False,user=user,items=items)


@app.route('/user/edit/profile/<user_id>',methods=['GET','POST'])
def user_editprofile(user_id):
    m=request.method
    
    def getUserEditProfile():
        user=getUser(user_id)
        return render_template('user_editprofile.html', isUser=True,isAuth=False,user=user)
    
    def postUserEditProfile():    
        d=request.form
        D={
            'user_id':user_id,
            'name':d['name'],
            'email':d['email'],
            'phoneno':d['phoneno'],
            'password':d['password']
        }
        ed=editUser(D)    
        if(ed):
            newUser=getUser(user_id)
            items=getPostBuyItemByUserId(user_id=user_id)
            success_message="Profile edited successfully"
            return render_template('user_profile.html',isUser=True,isAuth=False,success_message=success_message,user=newUser,items=items)
        else:
            items=getPostBuyItemByUserId(user_id=user_id)
            newUser=getUser(user_id)
            return render_template('user_profile.html',isUser=True,isAuth=False,error="Couldnt edit Profile,try again",user=newUser,items=items)
    return {
        'GET': getUserEditProfile,
        'POST': postUserEditProfile,
    }[m]()
        
@app.route('/user/search/<user_id>',methods=['GET','POST'])
def user_search(user_id=''):
    user=getUser(user_id=user_id)
    m=request.method
    def validate_input(filter_value, search_value):
        if filter_value == 'category_name' or filter_value == 'item_name':
            if not search_value.replace(' ', '').isalpha():
                return False

        elif filter_value == 'item_price':
            try:
                float_value = float(search_value)
                if not (0 <= float_value <= 999999.99) or search_value.count('.') > 1:
                    return False
            except ValueError:
                return False

        elif filter_value == 'manufacture_date':
            try:
                da = datetime.strptime(search_value, '%d-%m-%Y').date()
            except ValueError:
                return False

        return True

    def get():
        return render_template('user_search.html',user=user,isUser=True,isAuth=False,method=False)
    
    def post():
        d = request.form
        check=validate_input(filter_value=d['filter'],search_value=d['search'])
        if(d['filter']=='category_name'):
            if(check):
                categories = getAllCategory()
                search_term = d['search'].strip()
                final_products = []
                d={}
                cidarr=[]
                items=[]
                for category in categories:
                    flag=False
                    se=search_term.lower()
                    ce=category.cname.lower()
                    arr=se.split(' ')
                    for i in arr:
                        if i in ce:
                            flag=True
                    if(flag):
                        d[category.cid]=[]
                        final_products.append(category)
                        cidarr.append(category.cid)

                allitems=getAllItem()
                for item in allitems:
                    if item.category_id in cidarr:
                        items.append(item)
                        d[item.category_id].append(item)
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,final_products=final_products,method='category',items=items,d=d)
    
            else:
                error= "invalid text input"
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,error=error,method=False)
    
        elif(d['filter']=='item_name'):
            if(check):
                items=getAllItem()
                search_term = d['search'].strip()
                final_products= []
                for item in items:
                    flag=False
                    se=search_term.lower()
                    ce=item.name.lower()
                    arr=se.split(' ')
                    for i in arr:
                        if i in ce:
                            flag=True
                    if(flag):
                        final_products.append(item)
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,final_products=final_products,method='item')
            else:
                error= "inalid text input"
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,error=error,method=False)
        
        elif d['filter']=='item_price':
            if(check):
                items=getAllItem()
                final_products=[]
                search_term = d['search'].strip()
                for item in items:
                    if item.unit_price<=float(search_term):
                        final_products.append(item)
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,final_products=final_products,method='item')
            else:
                error= "inValid number input"
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,error=error,method=False)

        elif d['filter']=='manufacture_date':
            if(check):
                items=getAllItem()
                final_products = []
                search_term = d['search']
                search_date = datetime.strptime(search_term, '%d-%m-%Y').date()
                for item in items:
                    if item.mdate >= search_date:
                        final_products.append(item)

                return render_template('user_search.html', user=user, isUser=True, isAuth=False, final_products=final_products, method='item')


            else:
                error= "inValid date input, enter in 'dd-mm-yyyy' format"
                return render_template('user_search.html',user=user,isUser=True,isAuth=False,error=error,method=False)
    
        
    return {
        'GET': get,
        'POST': post,
    }[m]()

@app.route('/user/cart/<user_id>',methods=['GET','POST'])
def user_cart(user_id):
    success_message = request.args.get('success_message')
    
    user=getUser(user_id)
    cart=getCartsByUserId(user_id=user_id)
    if(cart):
        itemsCart=ListItemsInCart(cart_id=cart.cart_id)
        if(itemsCart):
            tot=totalPriceOfCart(cart_id=cart.cart_id)
        else:
            tot=0
    else:
        itemsCart=False
    Categories = db.session.query(Category).all()
    Items = db.session.query(Item).all()
    categories={}
    items={}
    for category in Categories:
        categories[category.cid]=category.cname
    for item in Items:
        items[item.item_id]={
            'name':item.name,
            'unit':item.unit,
            'unit_price':item.unit_price
            }
    leng=len(itemsCart)
    return render_template('user_cart.html',isUser=True,isAuth=False,user=user,cart=cart,itemsCart=itemsCart,tot=tot,categories=categories,items=items,leng=leng,success_message=success_message)

flag=0
@app.route('/user/buy/item/<user_id>/<item_id>',methods=['GET','POST'])
def user_buyitem(user_id,item_id):
    m=request.method
    user=getUser(user_id=user_id)
    cart=getCartsByUserId(user_id=user.user_id)
    
    def getBuyItem():
        global flag 
        flag=0
        item=getItem(item_id=item_id)
        category=getCategory(cid=item.category_id)
        return render_template('user_buyitem.html',isUser=True,isAuth=False,user=user,cart=cart,item=item,category=category,flag=flag,tot=0,quan=0)
    
    def postBuyItem():
        global flag
        d=request.form
        if flag==0:
            flag=1
            item=getItem(item_id=item_id)
            tot=float(d['quantity'])*float(item.unit_price)
            category=getCategory(cid=item.category_id)
            return render_template('user_buyitem.html',isUser=True,isAuth=False,user=user,cart=cart,item=item,category=category,flag=flag,tot=tot,quan=d['quantity'])
        else:
            item=getItem(item_id=item_id)
            category=getCategory(cid=item.category_id)
            
            D = {
                'cart_id': cart.cart_id,
                'category_id': item.category_id,
                'item_id': item.item_id,
                'qty_bought': float(d['total'])/float(item.unit_price),
                'total_price':float(d['total'])
            }
            new_cart_item=createCartItem(D)
            if(new_cart_item):
                success_message="Added to cart succesffuly"
                categories = db.session.query(Category).all()
                items = db.session.query(Item).all()
                d = {}
                for category in categories:
                    d[category.cid] = []

                for item in items:
                    d[item.category_id].append(item)
                return render_template('user_home.html', isUser=True,isAuth=False,d=d,categories=categories,items=items,user=user,success_message=success_message)
       
    return{
        'GET':getBuyItem,
        'POST':postBuyItem
    }[m]()




flag=0
@app.route('/user/edit/cart/item/<user_id>/<item_id>/<cart_item_no>/<cart_id>',methods=['GET','POST'])
def user_editcartitem(user_id,item_id,cart_item_no,cart_id):
    m=request.method
    user=getUser(user_id=user_id)
    cart=getCartsByUserId(user_id=user.user_id)
    
    def getEditCartItem():
        global flag 
        flag=0
        item=getItem(item_id=item_id)
        category=getCategory(cid=item.category_id)
        return render_template('user_editcartitem.html',isUser=True,isAuth=False,user=user,cart=cart,item=item,category=category,flag=flag,tot=0,quan=0,cart_id=cart_id,cart_item_no=cart_item_no)
    
    def postEditCartItem():
        global flag
        d=request.form
        if flag==0:
            flag=1
            tot=float(d['quantity'])*float(d['price'])
            item=getItem(item_id=item_id)
            category=getCategory(cid=item.category_id)
            return render_template('user_editcartitem.html',isUser=True,isAuth=False,user=user,cart=cart,item=item,category=category,flag=flag,tot=tot,quan=d['quantity'],cart_id=cart_id,cart_item_no=cart_item_no)
        else:
            item=getItem(item_id=item_id)
            category=getCategory(cid=item.category_id)
            D = {
                'cart_item_no':cart_item_no,
                'cart_id': cart.cart_id,
                'category_id': item.category_id,
                'item_id': item.item_id,
                'qty_bought': float(d['total'])/float(d['price']),
                'total_price':float(d['total'])
            }
            new_cart_item=editCartItem(D)
            if(new_cart_item):
                success_message = "Edited cart item successfully"                
                return redirect(url_for('user_cart',isUser=True,isAuth=False, user_id=user.user_id, success_message=success_message))
    return{
        'GET':getEditCartItem,
        'POST':postEditCartItem
    }[m]()

@app.route('/user/delete/cart/item/<user_id>/<item_id>/<cart_item_no>/<cart_id>',methods=['GET','POST'])
def user_deletecartitem(user_id,item_id,cart_item_no,cart_id):
    dele=deleteCartItem(cart_item_no=cart_item_no)
    if(dele):
        success_message="Item removed from the cart successfully"
        return redirect(url_for('user_cart', user_id=user_id,isUser=True,isAuth=False, success_message=success_message))
    else:
        error="Couldnt delete item"
        return redirect(url_for('user_cart', user_id=user_id, isUser=True,isAuth=False,error=error))

@app.route('/user/buy/all/<user_id>',methods=['GET','POST'])
def user_buyall(user_id):
    user=getUser(user_id=user_id)
    cart=getCartsByUserId(user_id=user_id)
    itemsCart=ListItemsInCart(cart_id=cart.cart_id)
    total=totalPriceOfCart(cart_id=cart.cart_id)
    D={
        'user_id':user_id,
        'total':total
        }
    cre=createPostbuy(D)
    for item in itemsCart:
        ditem=getItem(item.item_id)
        temp=float(ditem.qty)-float(item.qty_bought)
        
        d={
            'item_id':ditem.item_id,
            'category_id':ditem.category_id,
            'name':ditem.name,
            'unit':ditem.unit,
            'unit_price':ditem.unit_price,
            'qty':ditem.qty,
            'qty_left':temp,
            'mdate':ditem.mdate
        }
        dele=editItem(d)
        dele2=deleteCartItem(cart_item_no=item.cart_item_no)
        
    if(dele and dele2 and cre):
        success_message="Items Bought Successfully"
        return redirect(url_for('user_cart', user_id=user_id,isUser=True,isAuth=False, success_message=success_message))
    else:
        error="Couldnt buy item, try again"
        return redirect(url_for('user_cart', user_id=user_id, isUser=True,isAuth=False,error=error))
                    
@app.route('/user/logout')
def user_logout():
    res = make_response(redirect(url_for('user_login')))
    res.delete_cookie('token')
    return res
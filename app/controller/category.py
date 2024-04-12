from ..utils import db
from ..models import Category,Item

def createCategory(data={}):
    if getCategory(data['cname']):
        return None
    else:
        try:
            new_category = Category( 
                cname=data['cname']
            )
            db.session.add(new_category)
        except:
            db.session.rollback()
            raise Exception('DB error.')
        else:
            db.session.commit()
            return new_category

def deleteCategory(cid=''):
    try:
        
        item_delete_count = Item.query.filter(Item.category_id == cid).delete()
        category_delete_count = Category.query.filter(Category.cid == cid).delete()
        db.session.commit()
        
        if item_delete_count > 0 or category_delete_count > 0:
            return True
        else:
            return False
    except Exception as e:
        db.session.rollback()
        return False


def editCategory(data={}):
    try:
        categ = getCategory(cid=data['cid'])
        del data['cid']
        for key in data:
            setattr(categ, key, data[key])
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True

def getAllCategory():
    return db.session.query(Category).all()

def getCategory(cid='', cname=''):
    categ = db.session.query(Category).filter((Category.cid ==cid) | (Category.cname == cname)).first()
    return categ
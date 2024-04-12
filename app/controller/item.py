from ..utils import db 
from ..models import Item


def createItem(data={}):
    if getItemByName(data['name']):
        return None
    else:
        try:
            new_item=Item (
                category_id=data['category_id'],
                name=data['name'],
                unit=data['unit'],
                unit_price=data['unit_price'],
                qty=data['qty'],
                qty_left=data['qty_left'],
                mdate=data['mdate']
            )
            db.session.add(new_item)
        except:
            db.session.rollback()
            raise Exception('DB ERROR')
        else:
            db.session.commit()
            return new_item

def editItem(data={}):
    try:
        items= db.session.query(Item).filter((Item.item_id == data['item_id'])).first()
        del data['item_id']
        del data['category_id']
        for key in data:
            setattr(items,key,data[key])
    except:
        db.session.rollback()
        raise Exception('Error while editing Item')
    else:
        db.session.commit()
        return True

def getItem(item_id=''):
    items=db.session.query(Item).filter((Item.item_id==item_id)).first()
    return items

def getAllItem():
    return db.session.query(Item).all()

def getItemByName(name=''):
    items=db.session.query(Item).filter((Item.name==name)).first()
    return items

def deleteItem(item_id=''):
    Item.query.filter_by(item_id=item_id).delete()
    db.session.commit()
    return True

from ..utils import db
from ..models import CartItem,Item

def createCartItem(data={}):
    
    try:
        items=db.session.query(Item).filter(Item.item_id==data['item_id']).first()

        new_cart_item=CartItem(
            cart_id=data['cart_id'],
            category_id=data['category_id'],
            item_id=data['item_id'],
            qty_bought=data['qty_bought'],
            total_price=float(items.unit_price)*float(data['qty_bought'])                                           
        )
        db.session.add(new_cart_item)
    except:
        db.session.rollback()
        raise Exception('Error while Creating cart item')
    else:
        db.session.commit()
        return True
    
def editCartItem(data={}):
    try:
        cartItems=db.session.query(CartItem).filter(CartItem.cart_item_no==data['cart_item_no']).first()

        del data['cart_item_no']
        for key in data:
            setattr(cartItems,key,data[key])
    except:
        db.session.rollback()
        raise Exception('Error updating the items in cart')
    else:
        db.session.commit()
        return True
def deleteCartItem(cart_item_no=''):
    try:
        CartItem.query.filter(CartItem.cart_item_no==cart_item_no).delete()
        
    except:
        db.session.rollback()
        raise Exception('Error while deleting the cart item')
        
    else:
        db.session.commit()
        return True    
    
def deleteCartItemByItemId(item_id=''):
    try:
        items = db.session.query(CartItem).filter(CartItem.item_id == item_id).all() 
        if not items:
            return True  
        
        for item in items:
            db.session.delete(item) 
        db.session.commit()  
        return True  
    except Exception as e:
        
        return False 


def changePriceofItem(item_id='', unit_price=''):
    items = db.session.query(CartItem).filter(CartItem.item_id == item_id).all()

    if not items:
        return True

    for item in items:
        price = float(item.qty_bought) * float(unit_price)
        setattr(item, 'total_price', price)

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating price: {e}")
        return False 

def ListItemsInCart(cart_id=''):
    allitems = db.session.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    return allitems

def totalPriceOfCart(cart_id=''):
    allCartItems=db.session.query(CartItem).filter(CartItem.cart_id==cart_id).all()
    tot=0
    for i in allCartItems:
        tot+=i.total_price
    return tot
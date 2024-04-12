from ..utils import db 
from ..models import User,Cart

def createCart(data={}):
    try:
        new_cart=Cart(
        user_id=data['user_id']
        )
        db.session.add(new_cart)
    except:
        db.session.rollback()
        raise Exception('Error while Creating cart')
    else:
        db.session.commit()
        return new_cart

def getCartsByUserId(user_id):
    cart=db.session.query(Cart).filter(Cart.user_id==user_id).first()
    
    return cart

def deleteCart(cart_id=''):
    Cart.query.filter_by(cart_id=cart_id).delete()
    db.session.commit()
    return True

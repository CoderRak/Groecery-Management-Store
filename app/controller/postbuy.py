from ..utils import db 
from ..models import Postbuy

def createPostbuy(data={}):
    try:
        new_postbuy=Postbuy (
            user_id=data['user_id'],
            total=data['total']
        )
        db.session.add(new_postbuy)
    except:
        db.session.rollback()
        raise Exception('DB ERROR')
    else:
        db.session.commit()
        return new_postbuy

def getPostBuyItemByUserId(user_id=''):
    try:
        PostBuyItems=db.session.query(Postbuy).filter(Postbuy.user_id==user_id).all()
        return PostBuyItems
    except:
        return False
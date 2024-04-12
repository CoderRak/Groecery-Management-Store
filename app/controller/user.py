from ..utils import db
from ..models import User
from ..utils import custom_encrypt

def createUser(data={}):
    if getUser(data['email']):
        return None
    else:
        try:
            new_user = User( 
                name=data['name'],  
                email=data['email'],
                password=custom_encrypt(string=data['password']),
                phoneno=data['phoneno'],
            )
            db.session.add(new_user)
        except:
            db.session.rollback()
            raise Exception('DB error.')
        else:
            db.session.commit()
            return new_user

def deleteUser(user_id=''):
    User.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return True

def editUser(data={}):
    try:
        user = getUser(user_id=data['user_id'])
        del data['user_id']
        for key in data:
            setattr(user, key, data[key])
        
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True


def getUser(user_id='', email=''):
    user = db.session.query(User).filter((User.user_id == user_id) | (User.email == email)).first()
    return user
from ..utils import db
from ..models import Manager
from ..utils import custom_encrypt

def createManager(data={}):
    if getManager(data['email']):
        return None
    else:
        try:
            new_user = Manager( 
                name=data['name'],
                email=data['email'], 
                password=custom_encrypt(string=data['password'])
            )
            db.session.add(new_user)
        except:
            db.session.rollback()
            raise Exception('DB error.')
        else:
            db.session.commit()
            return new_user

def deleteManager(manager_id=''):
    Manager.query.filter_by(manager_id=manager_id).delete()
    db.session.commit()
    return True

def editManager(data={}):
    try:
        user = getManager(manager_id=data['manager_id'])
        del data['uid']
        for key in data:
            setattr(user, key, data[key])
        
    except:
        db.session.rollback()
        raise Exception('DB error.')
    else:
        db.session.commit()
        return True


def getManager(manager_id='', email=''):
    
    user = db.session.query(Manager).filter((Manager.manager_id == manager_id) | (Manager.email == email)).first()
    
    return user

def getMetrics():
    return ''
from ..utils import db 

class Postbuy(db.Model):
    __tablename__ = 'postbuy'
    postbuyno = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)
    user_id = db.Column(db.String(255) ,nullable=False)
    total = db.Column(db.String(255), nullable=False)
    
from ..utils import db

class Category(db.Model):
    __tablename__ = 'category'
    cid = db.Column(db.Integer,autoincrement=True, primary_key=True,nullable=False)
    cname = db.Column(db.String(255), nullable=False)

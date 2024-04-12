from ..utils import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,autoincrement=True, primary_key=True,nullable=False)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    phoneno = db.Column(db.Integer,nullable=False)

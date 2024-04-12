from ..utils import db

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', backref='carts')

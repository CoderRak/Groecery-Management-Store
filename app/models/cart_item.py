from ..utils import db

class CartItem(db.Model):
    __tablename__ = 'cart_item'
    cart_item_no = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id', ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.cid', ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id', ondelete="CASCADE"), nullable=False)
    qty_bought = db.Column(db.Integer ,nullable=False)
    total_price = db.Column(db.Integer ,nullable=False)
    cart = db.relationship('Cart', backref='cart_items')
    category = db.relationship('Category', backref='cart_items')
    item = db.relationship('Item', backref='cart_items')

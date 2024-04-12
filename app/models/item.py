from ..utils import db

class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True,nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.cid', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(255) ,nullable=False)
    unit = db.Column(db.String(50) ,nullable=False)
    unit_price = db.Column(db.Integer,nullable=False)
    qty = db.Column(db.Integer,nullable=False)
    qty_left=db.Column(db.Integer)
    mdate = db.Column(db.Date, nullable=False)
    category = db.relationship('Category', backref='items')

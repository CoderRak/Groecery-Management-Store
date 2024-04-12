from flask_restful import Resource, reqparse, fields, marshal_with
from ..utils import ValidationError, NotFoundError
from ..controller import createItem,editItem,deleteItem,getItem,getAllItem

create_item_parser = reqparse.RequestParser()
create_item_parser.add_argument('category_id')
create_item_parser.add_argument('description')
create_item_parser.add_argument('name')
create_item_parser.add_argument('unit')
create_item_parser.add_argument('unit_price')
create_item_parser.add_argument('qty')
create_item_parser.add_argument('qty_left')
create_item_parser.add_argument('mdate')

item_fields = {
    'item_id': fields.Integer,
    'category_id': fields.Integer,
    'name': fields.String,
    'unit': fields.String,
    'unit_price': fields.Integer,
    'qty': fields.Integer,
    'qty_left': fields.Integer,
    'mdate': fields.String(attribute=lambda x: x.mdate.strftime('%Y-%m-%d')),   
}

class ItemAPI(Resource):
    @marshal_with(item_fields)
    def get(self, item_id=None):
        item = None
        if not (item_id is None):
            item = getItem(item_id=item_id)
            if not item:
                raise NotFoundError()
        else:
            item = getAllItem()
        return item
    
    def put(self, item_id):
        args = create_item_parser.parse_args()
        category_id = args.get("category_id", None)
        name = args.get("name", None)
        unit = args.get("unit", None)
        unit_price = args.get("unit_price", None)
        qty = args.get("qty", None)
        qty_left = args.get("qty_left", None)
        mdate = args.get("mdate", None)
        
        if item_id is None:
            raise ValidationError(code=400, message="No Item ID provided")
        
        if category_id is None:
            raise ValidationError(code=400, message="No Category_id provided")
        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if unit is None:
            raise ValidationError(code=400, message="No unit provided")
        
        if unit_price is None:
            raise ValidationError(code=400, message="No unit_price provided")
        
        if  qty is None:
            raise ValidationError(code=400, message="No qty provided")
        
        if qty_left is None:
            raise ValidationError(code=400, message="No qty_left provided")
        
        if mdate is None:
            raise ValidationError(code=400, message="No mdate provided")
        

        data = dict()
        data['item_id'] = item_id
        data['category_id'] = category_id
        data['name'] = name
        data['unit'] = unit
        data['unit_price'] = unit_price
        data['qty'] = qty
        data['qty_left'] = qty_left
        data['mdate'] = mdate
        
        item = editItem(data)

        if item:
            return {'message': 'Item updated'}
    
    def delete(self, item_id):
        deleted = deleteItem(item_id=item_id)
        if (deleted):
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Something went wrong'}
    
    @marshal_with(item_fields)
    def post(self):
        args = create_item_parser.parse_args()
        category_id = args.get("category_id", None)
        name = args.get("name", None)
        unit = args.get("unit", None)
        unit_price = args.get("unit_price", None)
        qty = args.get("qty", None)
        qty_left = args.get("qty_left", None)
        mdate=args.get("mdate",None)

        if category_id is None:
            raise ValidationError(code=400, message="No Category_id provided")
        
        if name is None:
            raise ValidationError(code=400, message="No name provided")
        
        if unit is None:
            raise ValidationError(code=400, message="No unit provided")
        
        if unit_price is None:
            raise ValidationError(code=400, message="No unit_price provided")
        
        if qty is None:
            raise ValidationError(code=400, message="No qty provided")
        
        if qty_left is None:
            raise ValidationError(code=400, message="No qty_left provided")
        
        if mdate is None:
            raise ValidationError(code=400, message="No mdate provided")
        
        data = dict()
        data['categoery_id'] = category_id
        data['name'] = name
        data['unit'] = unit
        data['unit_price'] = unit_price
        data['qty'] = qty
        data['qty_left'] = qty_left
        data['mdate'] = mdate
        new_item = createItem(data)

        return new_item


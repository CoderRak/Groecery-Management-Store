from flask_restful import Resource, reqparse, fields, marshal_with
from ..utils import ValidationError, NotFoundError
from ..controller import createCategory,deleteCategory,editCategory,getAllCategory,getCategory


create_category_parser = reqparse.RequestParser()
create_category_parser.add_argument('cname')

category_fields = {
    'cid': fields.Integer,
    'cname': fields.String,
}

class CategoryAPI(Resource):
    @marshal_with(category_fields)
    def get(self, cid=None):
        category = None
        if not (cid is None):
            category = getCategory(cid=cid)
            if not category:
                raise NotFoundError()
        else:
            category = getAllCategory()
        return category
        
    def put(self, cid):
        args = create_category_parser.parse_args()
        cname = args.get("cname", None)

        if cid is None:
            raise ValidationError(code=400, message="No Category ID provided")
        
        if cname is None:
            raise ValidationError(code=400, message="No Category name provided")
        
        data = dict()
        data['cid'] = cid
        data['cname'] = cname
        category = editCategory(data)

        if category:
            return {'message': 'Category updated'}
    
    def delete(self, cid):
        deleted = deleteCategory(cid=cid)
        if (deleted):
            return {'message': 'Category deleted'}
        else:
            return {'message': 'Something went wrong'}
    
    @marshal_with(category_fields)
    def post(self):
        args = create_category_parser.parse_args()
        cname = args.get("cname", None)
        
        if cname is None:
            raise ValidationError(code=400, message="No Category name provided")
        
        data = dict()
        data['cname'] = cname
        new_category = createCategory(data)

        return new_category
from werkzeug.exceptions import HTTPException
from flask import make_response
import json

class ValidationError(HTTPException):
    def __init__(self, code, message):
        data = { "code" : code, "message": message }
        self.response = make_response(json.dumps(data), code)

class NotFoundError(ValidationError):
    def __init__(self):
        super().__init__(code=404, message='Resource not found')



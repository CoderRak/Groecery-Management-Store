from flask import current_app as app,make_response
from ..utils import tokenize

def authorizeUser(user, action, role='user'):
    res = make_response(action())
    token = tokenize(user=user, role=role)
    res.set_cookie('token', token)
    return res


from .config import Configuration as Config
from base64 import b64encode, b64decode
from cryptography.fernet import Fernet, InvalidToken
import time
import json

def custom_encrypt(string='', key=Config.SECRET_KEY):
    key = bytes(key, 'utf-8')

    fer = Fernet(key=key)
    
    string = fer.encrypt(data=bytes(string, 'utf-8'))
    string = b64encode(string)
    return string


def custom_decrypt(string='', key=Config.SECRET_KEY):
    key = bytes(key, 'utf-8')

    string = b64decode(string)
    fer = Fernet(key=key)

    try:
        string = fer.decrypt(token=string)
    except InvalidToken as e:
        raise Exception("Encryption error")
    
    string = string.decode('utf-8')
    return string

def tokenize(user, role=''):
    if role=='manager':
        d = {
        'id': user.manager_id,
        'name': user.name,
        'role': role,
        'ttl': (time.time_ns() + (86400000000000*2))
         }
    elif role=='user':
        d = {
        'id': user.user_id,
        'name': user.name,
        'role': role,
        'ttl': (time.time_ns() + (86400000000000*2))
    }
    return custom_encrypt(string=json.dumps(d)).decode('utf-8')

def detokenize(token):
    d = json.loads(custom_decrypt(string=token))
    return d

def validToken(token):
    d = detokenize(token)
    return d['ttl'] > time.time_ns()
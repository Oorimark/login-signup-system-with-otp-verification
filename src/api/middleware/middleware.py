import os
import requests
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

def validate_client_middleware(f):
    """ validates the clients using a access secret key """
    @wraps(f)
    def wrapper(*args, **kwargs):
        client_access_secret_key = request.headers.get('client_access_key')
        if client_access_secret_key == os.getenv('ACCESS_SECRET_KEY'):
            return f(*args, **kwargs)
        return jsonify({'err': 'client access secret key is invalid. Please contact the developer'})
    return wrapper

def validate_client_login_credentials(f):
    """ validate client login credentials """
    @wraps(f)
    def wrapper(*args, **kwargs):
        required_credentials: list[str] = ['email', 'password']
        for credential in request.json:
            if not credential in required_credentials:
                return jsonify({'data': {'err': f'{credential} is not provided.'}})
        return f(*args, **kwargs)
    return wrapper

def validate_client_signup_credentials(f):
    """ validate client login credentials """
    @wraps(f)
    def wrapper(*args, **kwargs):
        required_credentials: list[str] = ['name', 'email', 'password']
        for credential in request.json:
            if not credential in required_credentials:
                return jsonify({'data': {'err': f'{credential} is not provided.'}})
        return f(*args, **kwargs)
    return wrapper
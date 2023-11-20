import os
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


def validate_client_middleware(f):
    """ validates the clients using a access secret key """
    @wraps(f)
    def wrapper(*args, **kwargs):
        client_access_secret_key = request.headers.get('Client-Access-Key')
        if client_access_secret_key == os.getenv('ACCESS_SECRET_KEY'):
            return f(*args, **kwargs)
        return jsonify({'err': 'client access secret key is invalid. Please contact the developer'}), 404
    return wrapper


def validate_client_login_credentials(f):
    """ validate client login credentials """
    @wraps(f)
    def wrapper(*args, **kwargs):
        required_credentials: list[str] = ['email', 'password']
        if not list(request.json.keys()) == required_credentials:
            return jsonify({'data': {'err': f'Required keys(s) is not provided. Please read the documentation'}}), 404
        return f(*args, **kwargs)
    return wrapper


def validate_client_signup_credentials(f):
    """ validate client login credentials """
    @wraps(f)
    def wrapper(*args, **kwargs):
        required_credentials: list[str] = [
            'name', 'email', 'department', 'password']
        if not list(request.json.keys()) == required_credentials:
            return jsonify({'data': {'err': f'Required key(s) is not provided. Please read the documentation'}}), 404
        return f(*args, **kwargs)
    return wrapper

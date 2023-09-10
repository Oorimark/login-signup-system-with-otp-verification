from flask import Blueprint, jsonify, request
from middleware.middleware import validate_client_middleware, validate_client_login_credentials, validate_client_signup_credentials

# version 1 blueprint
api_v1 = Blueprint('v1_route', __name__, url_prefix = '/api/v1')

@api_v1.route('/client_login', methods=['POST'])
@validate_client_middleware
@validate_client_login_credentials
def client_login():
   ...

@api_v1.route('/client_login', methods=['POST'])
@validate_client_middleware
@validate_client_signup_credentials
def client_signup():
   ...
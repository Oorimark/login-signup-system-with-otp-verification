from flask import Blueprint, jsonify, request
from middleware.middleware import validate_client_middleware, validate_client_login_credentials, validate_client_signup_credentials
from services.auth.auth import auth_client_credential
from services.mail.mail_service import send_mail
from services.otp.otp_service import OTP_SERVICE

# version 1 blueprint
api_v1 = Blueprint('v1_route', __name__, url_prefix = '/api/v1')

""" client login route """
@api_v1.route('/client_login', methods=['POST'])
@validate_client_middleware
@validate_client_login_credentials
def client_login():
   # PROCESS
   # 1. check if password for the username (email) exist
   # 2. send a session token and the user id so the client can access
   auth_client_res = auth_client_credential(request.json)
   if auth_client_res.valid:
      return jsonify({'data': {'res': {'id': auth_client_res.id}}})
   return jsonify({'data': {'err': 'user credential is invalid'}})

""" send client otp route """
@api_v1.route('/send_otp', methods=['POST'])
@validate_client_middleware
def send_client_otp():
   client_email = request.json['email']

   otp_service = OTP_SERVICE()
   otp_service.create_otp_package()

   send_mail(
      rcpt_email=client_email, 
      title='An OTP Verification is sent', 
      sender_msg=otp_service.prepare_otp_package_for_mailing()
   )

""" validate client otp route """
@api_v1.route('/validate_otp', methods=['POST'])
@validate_client_middleware
@validate_client_signup_credentials
def validate_client_otp():
   # 1. send otp to the email from client
   client_otp = request.json('otp')
   ...

""" client sign up route """
@api_v1.route('/sign_up', methods=['POST'])
@validate_client_middleware
@validate_client_signup_credentials
def client_signup():
   # 1. send otp to the email from client
   ...
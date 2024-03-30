# Read the api docs for more examples: https://postman.com/login-2u3b29b2

from flask import Blueprint, jsonify, request
from src.api.middleware.middleware import (
    validate_client_middleware,
    validate_client_login_credentials,
    validate_client_signup_credentials,
)
from src.model.database.db import DatabaseModel, ClientMessagingCollectionWorker
from src.config.config import userCollection, clientMessagingCollection
from src.services.auth.auth import auth_client_credential
from src.services.mail.mail_service import send_mail
from src.services.otp.otp_service import OTP_SERVICE

# version 1 blueprint
api_v1 = Blueprint("v1_route", __name__, url_prefix="/api/v1")


@api_v1.route("/api_loopback_test", methods=["POST", "GET"])
def loopback_test():
    return "API VERSION 1 IS RUNNING"


@api_v1.route("/client_login", methods=["POST"])
@validate_client_middleware
@validate_client_login_credentials
def client_login():
    """Client login route: Login route"""
    # auth client credentials
    auth_client_res = auth_client_credential(request.json)
    if auth_client_res["valid"]:
        return jsonify({"data": {"res": {"id": str(auth_client_res["id"])}}}), 200
    # auth client is invalid
    return jsonify({"data": {"err": "user credential is invalid"}}), 404


@api_v1.route("/send_otp", methods=["POST"])
@validate_client_middleware
def send_client_otp():
    """Send client OTP route: Sends otp to a specified mail"""
    otp_service = OTP_SERVICE()
    client_email = request.json["email"]
    try:
        send_mail(
            rcpt_email=client_email,
            title="An OTP Verification is sent",
            sender_msg=otp_service.prepare_otp_package_for_mailing(),
        )
    except Exception as e:
        return jsonify({"data": {"err": f"mail was not sent. {e}"}}), 500
    else:
        otp_service.create_otp_package()
        return jsonify({"data": {"res": "sent successfully"}}), 200


@api_v1.route("/validate_otp", methods=["POST"])
@validate_client_middleware
def validate_client_otp():
    """Validate client otp route"""
    otp_service = OTP_SERVICE()
    client_otp = request.json["otp"]

    if otp_service.validate_otp(client_otp):
        otp_service.delete_otp(client_otp)
        return jsonify({"data": {"res": "otp is valid"}}), 200

    # client otp is not valid
    return jsonify({"data": {"err": "invalid client otp"}}), 404


@api_v1.route("/check_client_email", methods=["POST"])
@validate_client_middleware
def check_client_email():
    """Checks if email address already exist"""
    userCollectionModel = DatabaseModel(userCollection, "user-collection")
    find_res = userCollectionModel.find_one(request.json)
    if find_res:
        return jsonify({"data": {"res": True}}), 200
    # client email doesn't exist
    return jsonify({"data": {"res": False}}), 200


@api_v1.route("/sign_up", methods=["POST"])
@validate_client_middleware
def client_signup():
    """Client sign up route"""
    userCollectionModel = DatabaseModel(userCollection, "user-collection")
    try:
        userCollectionModel.insert(request.json)
    except Exception as e:
        return jsonify({"data": {"err": f"error inserting to database. {e}"}}), 500
    else:
        return jsonify({"data": {"res": "account have been created"}}), 200


@api_v1.route("/client_messaging_channel", methods=["POST", "GET"])
@validate_client_middleware
def client_messaging_channel():
    """Client Messaging channel"""
    if request.method == "POST":
        messaging_collection = DatabaseModel(
            clientMessagingCollection, "client-messaging-collection"
        )

        try:
            messaging_collection.insert(request.json)
        except Exception as e:
            return jsonify({"data": {"err": f"error inserting to database. {e}"}}), 500
        else:
            return jsonify({"data": {"res": "message sent"}}), 200
    else:
        # request is get method
        try:
            client_messaging_worker = ClientMessagingCollectionWorker(request.json)
        except Exception as e:
            return jsonify(
                {"data": {"err": f"client messaging worker is not working. {e}"}}
            ), 500
        else:
            client_messaging_worker.search_messages()
            messages = client_messaging_worker.trim_search_messages()
            return jsonify(
                {
                    "data": {
                        "res": {
                            "messages": messages,
                        }
                    }
                }
            ), 200


@api_v1.route("/send_email", methods=["POST"])
def send_email_endpoint():
    recpt_email = request.json["email"]
    msg = request.json["msg"]
    title = request.json["title"]

    try:
        send_mail(recpt_email, title, msg)
        return jsonify({"res": "Success"})
    except:
        return jsonify({"err": "Unable to send mail"})

import logging
from flask import Flask
from flask_cors import CORS
from src.config.config import mail_config
from flask_mail import Mail
from src.api.v1 import api_v1

app: Flask = Flask(__name__)
CORS(app)

# registering blueprint
app.register_blueprint(api_v1)

# configuring mail with app
# app.config = mail_config

# setting up mail
mail: Mail = Mail(app)

# # setting up logger
logging_configuration = {
    'level': logging.DEBUG,
    'format': "%(asctime)s %{levelname}s %(message)s",
    'datefmt': "%Y-%m-%d %H:%M:%S",
    'filename': 'application_service_log.log',
}

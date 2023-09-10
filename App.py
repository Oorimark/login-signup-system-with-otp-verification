from flask import Flask
from config.config import mail_config
from flask_mail import Mail
from api.v1 import api_v1

app: Flask = Flask(__name__)

# registering blueprint
app.register_blueprint(api_v1)

# configuring mail with app
app.config = mail_config

# setting up mail
mail: Mail = Mail(app)
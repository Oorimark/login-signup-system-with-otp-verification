import os
from pymongo import MongoClient

# SETTING UP DATABASE CONNECTION
cluster = MongoClient(os.getenv('MONGO_URL'))
db = cluster[os.getenv('APPLICATION_NAME') + '_DATA_HOUSE']

# SETTING UP MAIL CONFIGURATION
mail_config = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 465,
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': os.getenv('CONFIG_MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('CONFIG_MAIL_PASSWORD'),
    'MAIL_DEFAULT_SENDER': (os.getenv('APPLICATION_NAME'), os.getenv('CONFIG_MAIL_USERNAME')),
    'MAIL_ASCII_ATTACHMENTS': False
}
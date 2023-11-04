import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


""" SETTING UP DATABASE CONNECTION """

connection_string = f"mongodb+srv://{os.getenv('DB_CONNECTION_USERNAME')}:{os.getenv('DB_CONNECTION_PASSWORD')}@cluster0.xcz3g.mongodb.net/?retryWrites=true&w=majority"

try:
    cluster = MongoClient(connection_string)
except Exception as e:
    print('MongoClient is not connected to mongo url')

db = cluster[os.getenv('APP_NAME') + '_DATA_HOUSE']

# collections
userCollection = db['Users']
clientMessagingCollection = db['MessageCollection']

""" SETTING UP MAIL CONFIGURATION """


class MAIL_CONFIG:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER: (os.getenv('APP_NAME'),
                          os.getenv('MAIL_USERNAME'))
    MAIL_ASCII_ATTACHMENTS = False

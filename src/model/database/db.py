import datetime
from werkzeug.security import generate_password_hash
from config.config import clientMessagingCollection

""" DATABASE COLLECTION MODELS """
class DatabaseModel:
    def __init__(self, collection):
        self.collection = collection
    def insert(self, data: dict):
        # using middlewares with their associated collection
        match(self.collection.__name__):
            case 'user_collection':
                data = UserCollectionMIddlewaresFactory.pre('insert', data)
        self.collection.insert_one(data)
    def __delete_one(self, id: str):
        self.collection.delete_one({"_id": id})
    def __find_one(self, credential: dict):
        """ find an item based on the credential """
        self.collection.find_one(credential)

class UserCollectionMIddlewaresFactory:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        match(action):
            case 'insert':
                data.password = generate_password_hash(data.password)
                return data

class ClientMessagingCollection:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        match(action):
            case 'insert':
                data['time_stamp'] = datetime.datetime()
                return data

class ClientMessagingCollection:
    collection = clientMessagingCollection
    def __init__(self, get_request_params):
        self.sender_id, self.receiver_id, self.prev_client_messages = get_request_params.values()
    def search_messages(self):
        search_res_1 = self.collection.find({'sender_id': self.sender_id}, {'receiver_id': self.receiver_id})
        search_res_2 = self.collection.find({'sender_id': self.receiver_id}, {'receiver_id': self.sender_id})
        self.searched_res = search_res_1 + search_res_2
    def sort_searched_messages(self):
        """ sorts searched messages by date """

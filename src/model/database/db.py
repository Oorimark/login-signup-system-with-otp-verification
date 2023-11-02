from datetime import datetime
from werkzeug.security import generate_password_hash
from config.config import clientMessagingCollection

""" DATABASE COLLECTION MODELS """
class DatabaseModel:
    def __init__(self, collection):
        self.collection = collection
    def insert(self, data: dict):
        # using middlewares with their associated collection
        match(self.collection.__name__):
            case 'userCollection':
                data = UserCollectionMIddlewaresFactory.pre('insert', data)
            case 'clientMessagingCollection':
                ...
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

class ClientMessagingMiddlewaresFactory:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        match(action):
            case 'insert':
                data['time_stamp'] = datetime.now()
                return data

class ClientMessagingCollectionWorker:
    collection = clientMessagingCollection
    def __init__(self, get_request_params):
        self.sender_id, self.receiver_id, self.prev_client_messages = get_request_params.values()
    def search_messages(self):
        search_res_1 = self.collection.find({'sender_id': self.sender_id}, {'receiver_id': self.receiver_id})
        search_res_2 = self.collection.find({'sender_id': self.receiver_id}, {'receiver_id': self.sender_id})
        self.searched_res = search_res_1 + search_res_2
    def sort_searched_messages(self):
        """ sorts searched messages by date. Tim sort is used """
        self.searched_res.sort(key=lambda searched_data: searched_data['time_stamp'])
    def trim_search_messages(self):
        """ cuts messages length based on the previous client messages length """
        return self.searched_res[self.prev_client_messages:]

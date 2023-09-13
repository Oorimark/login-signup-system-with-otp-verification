from werkzeug.security import generate_password_hash

""" DATABASE COLLECTION MODELS """
class DatabaseModel:
    def __init__(self, collection):
        self.collection = collection
    def __insert(self, data: dict):
        match(self.collection.__name__):
            case 'user_collection':
                data = UserCollectionSchema.pre('insert', data)
        self.collection.insert_one(data)
    def __delete_one(self, id: str):
        self.collection.delete_one({"_id": id})
    def __find_one(self, credential: dict):
        """ find an item based on the credential """
        self.collection.find_one(credential)

class UserCollectionSchema:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        match(action):
            case 'insert':
                data.password = generate_password_hash(data.password)
                return data
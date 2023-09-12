from werkzeug.security import check_password_hash, generate_password_hash

""" DATABASE COLLECTION MODELS """
class Database_Model:
    def __init__(self, collection):
        self.collection = collection
    def __insert(self, data: dict):
        match(self.collection.__name__):
            case 'user_collection':
                data = User_Collection_Schema.pre('insert', data)
        self.collection.insert_one(data)
    def __delete_one(self, id: str):
        self.collection.delete_one({"_id": id})

class User_Collection_Schema:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        match(action):
            case 'insert':
                data.password = generate_password_hash(data.password)
                return data
""" DATABASE COLLECTION MODELS """
class Database_Model:
    def __init__(self, collection):
        self.collection = collection
    def insert(self, data):
        self.collection.insert_one(data)
    def delete_one(self, id: str):
        self.collection.delete_one({"_id": id})

class User_Collection_Schema:
    def pre(self, action, callback):
        ...
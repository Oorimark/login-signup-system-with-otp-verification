import json
from pprint import pprint
from datetime import datetime
from werkzeug.security import generate_password_hash
from src.config.config import clientMessagingCollection
from src.util.util import date_adapter

""" DATABASE COLLECTION MODELS """


class DatabaseModel:
    def __init__(self, collection, collection_name):
        self.collection = collection
        self.collection_name = collection_name

    def insert(self, data: dict):
        # using middlewares with their associated collection
        if self.collection_name == 'user-collection':
            data = UserCollectionMIddlewaresFactory().pre(
                'insert', data
            )
        elif self.collection_name == 'client-messaging-collection':
            # extract the adviserID and the studentID
            adviserID = data['adviserID']
            studentID = data['studentID']
            queryIDs = {'adviserID': adviserID, 'studentID': studentID}

            # find database to see if it already exist
            search_res = self.find_one(queryIDs)

            if search_res:
                data = ClientMessagingMiddlewaresFactory().pre(
                    'update', data['chats'][0])

                previous_chats = dict(search_res)['chats']
                new_chats = [*previous_chats, data]
                self.update_one(queryIDs, {'chats': new_chats})
                return
            else:
                updated_chats = ClientMessagingMiddlewaresFactory().pre(
                    'insert', data['chats'][0])
                data['chats'] = [updated_chats]

        self.collection.insert_one(data)

    def find_one(self, credential: dict):
        """ find an item based on the credential """
        return self.collection.find_one(credential)

    def update_one(self, filter_criteria: dict, update_item: dict):
        self.collection.update_one(filter_criteria, {"$set": update_item})


class UserCollectionMIddlewaresFactory:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        if action == 'insert':
            data['password'] = generate_password_hash(data['password'])
            return data


class ClientMessagingMiddlewaresFactory:
    def pre(self, action, data):
        """ middlewares to be used with model actions """
        if action == 'insert':
            data['timeStamp'] = datetime.now()
            return data
        elif action == 'update':
            data['timeStamp'] = datetime.now()
            return data


class ClientMessagingCollectionWorker:
    collection = clientMessagingCollection

    def __init__(self, request_params):
        self.last_message_time = request_params['lastMessagingTime']
        del request_params['lastMessagingTime']
        self.search_params = request_params

    def search_messages(self):
        search_res = self.collection.find(self.search_params)
        self.current_chats = list(search_res)[0]['chats']

    def trim_search_messages(self):
        """ cuts messages length based on the previous client messages length """
        transformed_last_message_time = date_adapter(self.last_message_time)

        for idx, chat in enumerate(self.current_chats):
            if chat['timeStamp'] > transformed_last_message_time:
                pprint(self.current_chats[idx:])
                return self.current_chats[idx:]
        return []

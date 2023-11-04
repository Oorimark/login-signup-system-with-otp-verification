""" Authentication for client """
from werkzeug.security import check_password_hash
from src.config.config import userCollection
from src.model.database.db import DatabaseModel


def auth_client_credential(credentials: dict):
    """ authenticate client credential via user password """

    email, pwd = credentials.values()
    userCollectionModel = DatabaseModel(userCollection, 'user-collection')
    user_credentials = userCollectionModel.find_one({'email': email})

    print(user_credentials)

    user_id, __, __, user_hashed_pwd = user_credentials.values()  # id, email, name, pwd

    print(pwd, user_hashed_pwd)

    if check_password_hash(user_hashed_pwd, pwd):
        return {'valid': True, 'id': user_id}
    return {'valid': False}

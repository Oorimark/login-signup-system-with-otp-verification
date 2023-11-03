""" Authentication for client """
from werkzeug.security import check_password_hash
from src.config.config import userCollection
from src.model.database.db import DatabaseModel


def auth_client_credential(credentials: dict):
    """ authenticate client credential via user password """
    __, pwd = credentials.values()
    user_credentials = DatabaseModel(userCollection)
    user_id, __, __, user_hashed_pwd = user_credentials.values()  # id, email, name, pwd
    if check_password_hash(pwd, user_hashed_pwd):
        return {'valid': True, 'id': user_id}
    return {'valid': False}

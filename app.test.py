import unittest
from src.config.config import users_collection

class DatabaseModelTest(unittest.TestCase):
    def set_up(self) -> None:
        print('database model test is running...')
    def test_collection_name(self):
        print(users_collection.__name__)
        self.assertIs(users_collection.__name__, 'string')
    def tearDown(self) -> None:
        return super().tearDown()

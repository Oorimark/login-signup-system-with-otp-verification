""" OTP Service script """
import json
from random import randint, shuffle
import datetime

class OTP_SERVICE:
    def generate_otp(self) -> int:
        # Magic numbers are not important
        max_salt_value: int = 5
        ref_values: str = '0123456789'
        salt: int = randint(2, max_salt_value)
        shuffle(ref_values)
        otp = int(ref_values[:4] * salt)
        self.otp = otp
        return otp
    def create_otp_package(self) -> None:
        timestamp: datetime = datetime.time
        otp: int = self.generate_otp() | self.otp
        self.otp_package: dict = {'timestamp': timestamp, 'otp': otp}
        OTP_SERVICE_STORAGE_WORKER().save_data(self.otp_package)
    def validate_otp(self, otp: int):
        return True if OTP_SERVICE_STORAGE_WORKER().find_otp(otp) else False
    def delete_otp(self, otp: int) -> None:
        OTP_SERVICE_STORAGE_WORKER().delete_data(otp)
    def prepare_otp_package_for_mailing(self) -> str:
        msg: str = f'Your One Time Password is {self.otp}'
        return msg

class OTP_SERVICE_STORAGE_WORKER:
    """ OTP SERVICE STORAGE WORKER: store pending otp """

    file_name= 'pendingOTP.db'

    def __init__(self):
        if not json.loads(self.read_file()):
            with open(self.file_name, 'w') as db:
                db.write(json.dumps("[]", indent = 4))
    def read_file(self):
        with open(self.file_name) as db:
            data = db.read()
            return json.loads(data)
    def write_file(self, updated_content):
        with open(self.file_name, 'w') as db:
            db.write(json.dumps(updated_content))
    def save_data(self, data):
        db = json.loads(self.read_file())
        db.append(data) # prev_db_content = db
        self.write_file(json.dumps(db)) # update db
    def delete_data(self, otp: int):
        db = json.loads(self.read_file())
        updated_content = filter(lambda data: data['otp'] != otp, db)
        new_updated_content_bucket = list()
        for content in updated_content:
            new_updated_content_bucket.append(content)
        self.write_file(json.dumps(new_updated_content_bucket))
    def find_otp(self, otp: int) -> None | dict:
        db = json.loads(self.read_file())
        for data in db:
            if data['otp'] == otp:
                return data
    def clear(self):
        with open(self.file_name, 'w') as db:
            db.write(json.dumps('[]', indent = 4))

""" OTP Service script """
import json
from random import randint, shuffle
from datetime import datetime


class OTP_SERVICE:
    def __init__(self):
        self.otp_service_storage_worker_instance = OTP_SERVICE_STORAGE_WORKER()

    def generate_otp(self) -> int:
        # Magic numbers are not important
        max_salt_value: int = 5
        ref_values: str = '0123456789'
        salt: int = randint(2, max_salt_value)
        char_string = list(ref_values)
        shuffle(char_string)
        shuffled_string = ''.join(char_string)
        otp = int(shuffled_string[:4] * salt)
        self.otp = otp
        return str(otp)[:6]

    def create_otp_package(self) -> None:
        timestamp: datetime.time = datetime.now().time()
        otp: int = self.generate_otp()
        self.otp_package: dict = {
            'timestamp': (timestamp.isoformat()), 'otp': otp}
        self.otp_service_storage_worker_instance.save_data(self.otp_package)

    def validate_otp(self, otp: int):
        return True if self.otp_service_storage_worker_instance.find_otp(otp) else False

    def delete_otp(self, otp: int) -> None:
        self.otp_service_storage_worker_instance.delete_data(otp)

    def prepare_otp_package_for_mailing(self) -> str:
        msg: str = f'Your One Time Password is {self.otp}'
        return msg


class OTP_SERVICE_STORAGE_WORKER:
    """ OTP SERVICE STORAGE WORKER: store pending otp """

    file_name = 'pending_otp.db'

    def __init__(self):
        if not (self.read_file()):
            self.write_file([])

    def read_file(self):
        with open(self.file_name) as db:
            data = db.read()
            return json.loads(data) if data else data

    def write_file(self, updated_content):

        # print(type(json.dumps(updated_content)))

        with open(self.file_name, 'w') as db:
            print(type(updated_content))
            db.write(json.dumps(updated_content, indent=5))

    def save_data(self, data):
        db = self.read_file()
        db.append(data)
        self.write_file(db)  # update db

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
            db.write(json.dumps('[]', indent=4))

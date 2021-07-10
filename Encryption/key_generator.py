import hashlib
from datetime import datetime


class key_generator():

    def get_password_hash(self, password):
        if not isinstance(password, str):
            raise ValueError("filePath has to be of type string")

        bytes = bytearray()
        bytes.extend(map(ord, hashlib.sha512(
            password.encode("UTF-8")).hexdigest()))

        return bytes

    def get_random_hash(self):
        now = datetime.utcnow()
        rnd = (now - datetime(1, 1, 1)).total_seconds() * 10000000

        bytes = bytearray()
        bytes.extend(map(ord, hashlib.sha512(
            str(rnd).encode("UTF-8")).hexdigest()))

        return bytes

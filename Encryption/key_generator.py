import hashlib
from datetime import datetime


class key_generator():

    def get_password_hash(self, password: str) -> bytearray:
        bytes = bytearray()
        bytes.extend(map(ord, hashlib.sha512(
            password.encode("UTF-8")).hexdigest()))

        return bytes

    def get_random_hash(self) -> bytearray:
        now = datetime.utcnow()
        rnd = (now - datetime(1, 1, 1)).total_seconds() * 10000000

        bytes = bytearray()
        bytes.extend(map(ord, hashlib.sha512(
            str(rnd).encode("UTF-8")).hexdigest()))

        return bytes

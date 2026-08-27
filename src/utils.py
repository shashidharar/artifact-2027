
"""
============================================================
ARIA Research Prototype
Utility Functions
============================================================
"""

import hashlib
import json
import secrets
import time
import uuid


class CryptoUtils:

    @staticmethod
    def sha256(data):

        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)

        if not isinstance(data, str):
            data = str(data)

        return hashlib.sha256(data.encode()).hexdigest()


    @staticmethod
    def random_token():

        return str(uuid.uuid4())


    @staticmethod
    def nonce(length=16):

        return secrets.token_hex(length)


class TimeUtils:

    @staticmethod
    def now():

        return time.time()


    @staticmethod
    def timestamp():

        return int(time.time())


class JSONUtils:

    @staticmethod
    def save(data, filename):

        with open(filename, "w") as fp:

            json.dump(data, fp, indent=4)


    @staticmethod
    def load(filename):

        with open(filename, "r") as fp:

            return json.load(fp)


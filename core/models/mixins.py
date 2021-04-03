from os import urandom

from passlib.handlers.pbkdf2 import pbkdf2_sha256


class CryptMixin:
    SALT_LENGTH = 16

    @classmethod
    def hash(cls, password):
        settings = dict(
            rounds=3000,
            salt=urandom(cls.SALT_LENGTH),
        )
        return pbkdf2_sha256.using(**settings).hash(password)

    @staticmethod
    def verify(password, hash):
        return pbkdf2_sha256.verify(password, hash)

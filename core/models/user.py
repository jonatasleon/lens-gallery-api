from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from core.db import db

from .mixins import CryptMixin


class UserModel(db.Model, CryptMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(Text, unique=True)
    _password = Column("password", Text)
    photos = relationship("PhotoModel", backref="user", lazy=True)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = self.hash(password)

    def check_password(self, password: str) -> bool:
        return self.verify(password, self.password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"

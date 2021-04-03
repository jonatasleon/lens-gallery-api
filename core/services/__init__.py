import typing

from flask_jwt_extended.utils import create_access_token
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import IntegrityError, NoResultFound

from core.db import db
from core.models import PhotoModel, UserModel

T = typing.TypeVar("T")

class Service(typing.Generic[T]):
    __session__ = db.session
    __model__: T

    @classmethod
    def _get(cls, **filters):
        return cls.__model__.query.filter_by(**filters)

    @classmethod
    def get_one(cls, **filters) -> T:
        return cls._get(**filters).one()

    @classmethod
    def list(cls, **filters) -> typing.List[T]:
        return cls._get(**filters).all()


class LoginService(Service):
    __model__ = UserModel

    @classmethod
    def check_credentials(cls, credentials) -> bool:
        try:
            return cls.get_one(email=credentials.email) \
                      .check_password(credentials.password)
        except NoResultFound:
            return False

    @classmethod
    def get_access_token(cls, credentials) -> str:
        return create_access_token(identity=cls.get_one(email=credentials.email))


class UserService(Service):
    __model__ = UserModel

    @classmethod
    def get_by_id(cls, id) -> UserModel:
        return cls.get_one(id=id)

    @classmethod
    def save(cls, user: UserModel) -> UserModel:
        if user.id is None:
            try:
                cls.__session__.add(user)
            except IntegrityError:
                raise ValueError()
        else:
            cls.__session__.merge(user)
        cls.__session__.commit()
        return user

    @classmethod
    def remove(cls, id: int):
        photo = cls.get_by_id(id)
        cls.__session__.delete(photo)
        cls.__session__.commit()


class PhotoService(Service):
    __model__ = PhotoModel

    @classmethod
    def list(cls, user_id: int) -> typing.List[UserModel]:
        return super().list(user_id=user_id)

    @classmethod
    def get_by_id(cls, id: int, user_id: int) -> UserModel:
        return cls.get_one(id=id, user_id=user_id)

    @classmethod
    def save(cls, photo: PhotoModel) -> PhotoModel:
        if photo.id is None:
            cls.__session__.add(photo)
        else:
            cls.__session__.merge(photo)
        cls.__session__.commit()
        return photo

    @classmethod
    def remove(cls, id, user_id: int):
        photo = cls.get_by_id(id, user_id)
        cls.__session__.delete(photo)
        cls.__session__.commit()

from collections import namedtuple
from functools import wraps

from flask.json import jsonify
from marshmallow import Schema as BaseSchema
from marshmallow import fields
from marshmallow.decorators import post_load

from core.models import PhotoModel, UserModel
from core.utils import unpack


class Schema(BaseSchema):
    __model__ = None

    @classmethod
    def dump_with(cls, *fn_args, **fn_kwargs):
        """A decorator that apply dump to the return values of your methods."""

        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                resp = fn(*args, **kwargs)
                if isinstance(resp, tuple):
                    data, code, headers = unpack(resp)
                    result = (
                        jsonify(cls().dump(data, *fn_args, **fn_kwargs)),
                        code,
                        headers,
                    )
                else:
                    result = jsonify(cls().dump(resp, *fn_args, **fn_kwargs))
                return result

            return wrapper

        return decorator

    @post_load
    def make_object(self, data, **_):
        if self.__model__:
            return self.__model__(**data)
        return data


class UserSchema(Schema):
    __model__ = UserModel

    id = fields.Integer(dump_only=True)
    name = fields.String()
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class LoginSchema(Schema):
    __model__ = namedtuple("LoginModel", "email password")
    email = fields.Email(required=True, load_only=True)
    password = fields.String(required=True, load_only=True)


class PhotoSchema(Schema):
    __model__ = PhotoModel

    id = fields.Int(dump_only=True)
    title = fields.Str()
    url = fields.URL(required=True)
    description = fields.Str()

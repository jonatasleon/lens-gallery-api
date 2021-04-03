from functools import wraps


def unpack(value):
    """Return a three tuple of data, code, and headers"""
    if not isinstance(value, tuple):
        return value, 200, {}

    try:
        data, code, headers = value
        return data, code, headers
    except ValueError:
        pass

    try:
        data, code = value
        return data, code, {}
    except ValueError:
        pass

    return value, 200, {}


def parse_args_with_schema(schema):
    def decorator(fn):
        @wraps(fn)
        def wrapper(**kwargs):
            return fn(schema().load(kwargs))

        return wrapper

    return decorator

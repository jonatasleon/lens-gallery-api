import logging
import os
from logging.handlers import TimedRotatingFileHandler

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import Swagger
from flasgger.marshmallow_apispec import APISpec
from flasgger.utils import apispec_to_template
from flask import Flask

from . import models
from .commands import command_groups
from .db import db
from .security import cors, jwt
from .views import api_bp
from .config import get_config

__version__ = "0.0.1"
__title__ = "Lens Gallery API"


def create_app(env: str = "development"):
    app = Flask(__name__, static_folder=None)
    app.config["ENV"] = env
    app.config.from_object(get_config(env))
    app.config.from_envvar("APP_SETTINGS", silent=must_silent_envvar(env))

    api_spec = APISpec(
        title=__title__,
        version=__version__,
        openapi_version="2.0",
        plugins=[
            FlaskPlugin(),
            MarshmallowPlugin(schema_name_resolver=lambda schema: schema.__name__.replace("Schema", "")),
        ],
    )

    register_extensions(app)
    register_swagger(app, api_spec)
    register_blueprints(app)
    register_commands(app)
    register_logger(app)

    return app


def must_silent_envvar(env: str):
    return env != "production"


def register_extensions(app: Flask):
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    app.db = db


def register_swagger(app: Flask, api_spec: APISpec):
    template = apispec_to_template(app, api_spec)
    Swagger(app, template=template)


def register_blueprints(app: Flask):
    app.register_blueprint(api_bp)


def register_commands(app: Flask):
    for command in command_groups:
        app.cli.add_command(command)

    app.shell_context_processor(lambda: {"db": db, "models": models})


def register_logger(app):
    if not app.debug:
        # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
        file_handler = TimedRotatingFileHandler(os.path.join(app.config["LOG_DIR"], "core.log"), "midnight")
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter("<%(asctime)s> <%(levelname)s> %(message)s"))
        app.logger.addHandler(file_handler)

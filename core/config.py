import os


class Config:
    DEBUG = False
    TESTING = False
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_SECRET_KEY = "super-secret"
    LOG_DIR = "."
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    LOG_DIR = os.environ.get("LOG_DIR")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/temp.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


def get_config(env: str) -> Config:
    config = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "test": TestConfig,
    }

    return config.get(env, DevelopmentConfig)

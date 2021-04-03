import os


class Config:
    DEBUG = False
    JWT_ERROR_MESSAGE_KEY = "message"
    JWT_SECRET_KEY = "super-secret"
    LOG_DIR = "."
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(Config):
    ...


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

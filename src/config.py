"""Configs."""
import os
import logging
from abc import ABCMeta


class _SingletonMeta(ABCMeta):
    instance = None

    def __call__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance


class _Config(metaclass=_SingletonMeta):
    DEBUG = True
    RELOAD = True
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = os.getenv('PORT', 8000)
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secret")

    class DB_CONFIG:
        SQLALCHEMY_LOG = False


class _DevelopementConfig(_Config):
    DEBUG = True
    RELOAD = True
    LOG_LEVEL = logging.DEBUG


class _StagingConfig(_Config):
    DEBUG = True
    RELOAD = False
    LOG_LEVEL = logging.INFO


class _ProductionsConfig(_Config):
    DEBUG = False
    RELOAD = False
    LOG_LEVEL = logging.ERROR


_configs = {
    "dev": _DevelopementConfig,
    "stage": _StagingConfig,
    "prod": _ProductionsConfig
}

env = os.getenv("ENV", 'prod')

Configurations = _configs.get(env)

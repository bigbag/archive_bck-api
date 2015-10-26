# -*- coding: utf-8 -*-
import os

from web.helpers.logging_helper import setup_loggers

os_env = os.environ


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    APP_HOST = '0.0.0.0'
    APP_PORT = 7777

    # TIMEZONES
    TIME_ZONE = 'Europe/Moscow'

    # CSRF & SECRET_KEY
    BCRYPT_LOG_ROUNDS = 13

    # DEBUG
    DEBUG = False
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # DATABASES
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/web?charset=utf8'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # API
    API_PROJECT_NAME = 'bck-api'

    # LOGGING
    LOG_ENABLE = True
    LOG_LEVEL = 'ERROR'
    LOG_MAX_SIZE = 1024 * 1024
    LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
    LOG_SETTINGS = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(levelname)s] [P:%(process)d] [%(asctime)s] %(pathname)s:%(lineno)d: %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            },
            'simple': {
                'format': '[%(levelname)s] [P:%(process)d] [%(asctime)s] %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            },
        }
    }

    setup_loggers(LOG_SETTINGS, LOG_ENABLE, LOG_LEVEL, LOG_DIR, LOG_MAX_SIZE)


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    LOG_ENABLE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1

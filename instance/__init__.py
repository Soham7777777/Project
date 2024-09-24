from datetime import timedelta
from abc import ABC
import os

class IFlaskDefaultConfiguration(ABC):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = None
    TRAP_HTTP_EXCEPTIONS = False
    TRAP_BAD_REQUEST_ERRORS = None
    SECRET_KEY = None
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = None
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = None
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_REFRESH_EACH_REQUEST = True
    USE_X_SENDFILE = False
    SEND_FILE_MAX_AGE_DEFAULT = None
    SERVER_NAME = None
    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = 'http'
    MAX_CONTENT_LENGTH = None
    TEMPLATES_AUTO_RELOAD = None
    EXPLAIN_TEMPLATE_LOADING = False
    MAX_COOKIE_SIZE = 4093

class IApplicationConfiguration(IFlaskDefaultConfiguration):
    SECRET_KEY = os.getenv('SECRET_KEY') # type: ignore
    DEBUG=True
    TESTING=True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.db'
    SQLALCHEMY_ECHO=True

    MAIL_USERNAME = os.getenv('DEFAULT_SENDER_ADDRESS', 'None')
    MAIL_DEFAULT_SENDER = os.getenv('DEFAULT_SENDER_ADDRESS', 'None')
    MAIL_PASSWORD = os.getenv('GOOGLE_ACCOUNT_APP_PASSWORD', 'None')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    JWT_TOKEN_LOCATION = ['query_string']

    # CELERY = dict(
    #     broker_url="redis://localhost:6379",
    #     task_ignore_result=True,
    # )

    RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', 'NONE')
    RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', 'None')

    
class Development(IApplicationConfiguration):
    TESTING=False

class Testing(IApplicationConfiguration):
    DEBUG=False
    PROPAGATE_EXCEPTIONS = False # type: ignore

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO=False

class Deployment(IApplicationConfiguration):
    DEBUG=False
    TESTING=False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
    SQLALCHEMY_ECHO=False


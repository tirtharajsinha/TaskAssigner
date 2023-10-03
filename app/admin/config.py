# set your app config here


class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "hlky288dnp10eskj"
    FLASK_SECRET = SECRET_KEY
    # FLASK_HTPASSWD_PATH = '/secret/.htpasswd'

    # Database config
    SQLALCHEMY_DATABASE_URI = "sqlite:///registration.db"

    # Folder config
    STATIC_FOLDER = ("static",)
    TEMPLATE_FOLDER = "templates"

    # mail sender config
    MAIL_SERVER = "smtp-relay.brevo.com"
    MAIL_PORT = 587  # Change it
    MAIL_USERNAME = "sinhatirtharaj1@gmail.com"
    MAIL_PASSWORD = "c3fn9XQKbVDEP54G"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SECRET_KEY = "hlky288dnp10eskj"
    FLASK_SECRET = SECRET_KEY
    # FLASK_HTPASSWD_PATH = '/secret/.htpasswd'

    # Database config
    SQLALCHEMY_DATABASE_URI = "sqlite:///registration.db"

    # Folder config
    STATIC_FOLDER = ("static",)
    TEMPLATE_FOLDER = "templates"

    # mail sender config
    MAIL_SERVER = "<Use your mail server>"
    MAIL_PORT = 587  # Change it
    MAIL_USERNAME = "<USE Your mail id>"
    MAIL_PASSWORD = "<Your mail password/key>"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False

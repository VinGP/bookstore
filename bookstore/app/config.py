from environs import Env

env = Env()
env.read_env()


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = "SECRET_KEY"
    DATABASE_URL = f"postgresql://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    MAIL_SERVER = env.str("MAIL_SERVER", "localhost.local")
    MAIL_PORT = env.int("MAIL_PORT", 25)
    MAIL_USE_TLS = env.bool("MAIL_USE_TLS", False)
    MAIL_USERNAME = env.str("MAIL_USERNAME", "flask@localhost.local")
    MAIL_PASSWORD = env.str("MAIL_PASSWORD", "111")

    FLASK_ADMIN_FLUID_LAYOUT = True
    FLASK_ADMIN_SWATCH = "cerulean"
    FLASK_ADMIN_TEMPLATE_MODE = "bootstrap4"

    ELASTICSEARCH_URL = "http://elasticsearch:9200"

    PER_PAGE = 24

    YOOKASSA_ACCOUNT_ID = env.str("YOOKASSA_ACCOUNT_ID", None)
    YOOKASSA_SECRET_KEY = env.str("YOOKASSA_SECRET_KEY", None)

    DADATA_SECRET_KEY = env.str("DADATA_SECRET_KEY", None)
    DADATA_API_KEY = env.str("DADATA_API_KEY", None)

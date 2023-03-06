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

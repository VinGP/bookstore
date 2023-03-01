import os

from environs import Env

env = Env()
env.read_env()


class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "SECRET_KEY"
    # env.str("TELEGRAM_BOT_TOKEN")

    # DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{dbname}"
    # env.str('DB_NAME')
    DATABASE_URL = f"postgresql://{env.str('DB_USER')}:{env.str('DB_PASSWORD')}@{env.str('DB_HOST')}:{env.str('DB_PORT')}/{env.str('DB_NAME')}"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL

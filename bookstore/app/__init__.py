import os

from elasticsearch import Elasticsearch
from flask import Flask
from flask_babelex import Babel
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from werkzeug.middleware.proxy_fix import ProxyFix
from yookassa import Configuration, Payment
from yookassa.domain.exceptions.unauthorized_error import UnauthorizedError

from .config import Config
from .models import db_session

app = Flask(__name__)
app.config.from_object(Config)
file_path = os.path.join(os.path.dirname(__file__), "static")
db_session.global_init(app.config["SQLALCHEMY_DATABASE_URI"])
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1, x_proto=1, x_host=1)

if app.config["YOOKASSA_ACCOUNT_ID"] and app.config["YOOKASSA_SECRET_KEY"]:
    Configuration.account_id = app.config["YOOKASSA_ACCOUNT_ID"]
    Configuration.secret_key = app.config["YOOKASSA_SECRET_KEY"]
    try:
        Payment.list({"test": "rest"})
    except UnauthorizedError:
        print(
            "UnauthorizedError, Неправильный YOOKASSA_ACCOUNT_ID и YOOKASSA_SECRET_KEY"
        )
        Configuration.account_id = None
        Configuration.secret_key = None

app.elasticsearch = (
    Elasticsearch([app.config["ELASTICSEARCH_URL"]])
    if app.config["ELASTICSEARCH_URL"]
    else None
)

login_manager = LoginManager(app)

babel = Babel(app)

mail = Mail(app)

moment = Moment(app)

from app.admin import admin  # noqa

from . import auth  # noqa
from . import views  # noqa

admin.init_app(app)

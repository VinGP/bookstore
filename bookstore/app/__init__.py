import os.path as op

from flask import Flask
from flask_babelex import Babel
from flask_login import LoginManager
from flask_mail import Mail

from .config import Config
from .models import db_session

app = Flask(__name__)
app.config.from_object(Config)
file_path = op.join(op.dirname(__file__), "files")

db_session.global_init(app.config["SQLALCHEMY_DATABASE_URI"])
login_manager = LoginManager(app)

babel = Babel(app)

mail = Mail(app)

from app.admin import admin  # noqa

from . import auth  # noqa
from . import views  # noqa

admin.init_app(app)

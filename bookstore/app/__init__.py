from flask import Flask

# from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager

from .config import Config
from .models import db_session

app = Flask(__name__)
app.config.from_object(Config)
db_session.global_init(app.config["SQLALCHEMY_DATABASE_URI"])
login_manager = LoginManager(app)

babel = Babel(app)

from app.admin import admin  # noqa

from . import auth  # noqa
from . import routes  # noqa

admin.init_app(app)

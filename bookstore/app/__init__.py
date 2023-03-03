from flask import Flask
from flask_admin import Admin
from flask_babelex import Babel

from .config import Config
from .models import db_session

app = Flask(__name__)
app.config.from_object(Config)
db_session.global_init(app.config["SQLALCHEMY_DATABASE_URI"])

babel = Babel(app)

admin = Admin(app, name="BookStoreManager", template_mode="bootstrap4")

from . import routes

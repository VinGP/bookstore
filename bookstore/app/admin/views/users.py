from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.users import User

admin.add_view(MyBaseView(User, db_session.create_session()))

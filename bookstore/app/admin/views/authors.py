from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.authors import Author

admin.add_view(MyBaseView(Author, db_session.create_session(), name="Авторы"))

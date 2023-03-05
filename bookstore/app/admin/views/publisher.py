from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.publishers import Publisher

admin.add_view(MyBaseView(Publisher, db_session.create_session(), name="Издательства"))

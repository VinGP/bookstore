from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.orders import Order

admin.add_view(MyBaseView(Order, db_session.create_session(), name="Заказы"))

from app import app
from app.admin.views.base import MyBaseView
from app.admin.views.index import MyAdminIndexView
from flask_admin import Admin

admin = Admin(
    name="BookStoreManager",
    template_mode=app.config.get("FLASK_ADMIN_TEMPLATE_MODE", "bootstrap4"),
    index_view=MyAdminIndexView(),
    base_template="admin/my_master.html",
)

from app.admin.views import authors, books, categories, orders, publisher, users  # noqa

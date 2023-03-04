from app.admin.views.base import MyBaseView
from app.admin.views.index import MyAdminIndexView
from app.models import db_session
from app.models.authors import Author
from flask_admin import Admin

admin = Admin(
    name="BookStoreManager",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),
    base_template="admin/my_master.html",
)

from app.admin.views import authors, books, publisher, users  # noqa

from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.images import Image

# from app.models.users import User

# admin.add_view(MyBaseView(Image, db_session.create_session(), name="Картинки"))


class ImageView(MyBaseView):
    column_display_pk = True
    column_hide_backrefs = False
    column_display_all_relations = True
    # column_searchable_list = ["id", "name", "surname", "email",
    #                           "phone_number"]
    # column_filters = ["author", "publisher"]
    form_columns = ["id", "path"]

    column_list = ("id", "path")
    # column_labels = dict(id='ID', name="Имя", surname="Фамилия",
    #                      email="Электронная почта",
    #                      phone_number="Номер телефона",
    #                      )


admin.add_view(ImageView(Image, db_session.create_session(), name="Картинки"))

from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.users import User


class UserView(MyBaseView):
    column_display_pk = True
    column_hide_backrefs = False
    column_display_all_relations = True
    column_searchable_list = ["id", "name", "surname", "email", "phone_number"]
    # column_filters = ["author", "publisher"]
    form_columns = ["name", "surname", "email", "phone_number"]

    column_list = ("id", "name", "surname", "email", "phone_number")
    column_labels = dict(
        id="ID",
        name="Имя",
        surname="Фамилия",
        email="Электронная почта",
        phone_number="Номер телефона",
    )

    form_widget_args = {
        "id": {"readonly": True, "validators": []},
    }


admin.add_view(UserView(User, db_session.create_session(), name="Пользователи"))

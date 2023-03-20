from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.categories import Category


class CategoriesView(MyBaseView):
    column_sortable_list = ["name"]

    column_searchable_list = ["parent.name", "name"]

    column_filters = ["parent.name"]

    form_columns = [
        "name",
        "parent",
    ]
    column_labels = dict(
        parent="Над категория",
        name="Название",
    )
    column_list = [
        "name",
        "parent",
    ]

    def create_form(self, obj=None):
        return super(CategoriesView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(CategoriesView, self).edit_form(obj)

    def search_placeholder(self):
        return "Поиск по названию"


admin.add_view(CategoriesView(Category, db_session.create_session(), name="Категории"))

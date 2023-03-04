from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.books import Book


class BooksView(MyBaseView):
    column_display_pk = True
    column_hide_backrefs = False
    column_display_all_relations = True
    column_searchable_list = ["author.first_name", "title"]
    column_filters = ["author", "publisher"]
    form_columns = ["title", "author", "available_quantity", "price", "publisher"]

    column_list = ("id", "title", "author", "available_quantity", "price", "publisher")

    def search_placeholder(self):
        return "Поиск по названию и автору"


admin.add_view(BooksView(Book, db_session.create_session()))

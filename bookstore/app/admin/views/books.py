from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.books import Book
from flask import url_for
from flask_admin import form
from markupsafe import Markup


class BooksView(MyBaseView):
    column_display_pk = True
    column_hide_backrefs = False
    column_display_all_relations = True
    column_searchable_list = ["author.first_name", "title"]
    column_filters = ["author", "publisher"]
    form_columns = [
        "title",
        "author",
        "available_quantity",
        "price",
        "publisher",
        "images",
    ]

    column_list = (
        "id",
        "title",
        "author",
        "available_quantity",
        "price",
        "publisher",
        "images",
    )
    column_labels = dict(
        id="ID",
        title="Название",
        author="Автор",
        available_quantity="Количество экземпляров",
        publisher="Издательство",
        price="Цена",
    )

    def _list_thumbnail(view, context, model, name):
        print("11111", model.images[0])
        if not model.images:
            return ""
        try:
            # print("!!!", model.images.path)
            print(
                url_for("static", filename=form.thumbgen_filename(model.images[0].path))
            )
            print(url_for("static", filename="upload/" + model.images[0].path))
            return Markup(
                '<img src="%s">'
                % url_for("static", filename="upload/" + model.images[0].path)
            )
        except Exception as e:
            print(e)
            return "her"

    column_formatters = {"images": _list_thumbnail}

    #
    # # Alternative way to contribute field is to override it completely.
    # # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    # form_extra_fields = {
    #     'images': form.ImageUploadField('Image',
    #                                     base_path=file_path,
    #                                     thumbnail_size=(100, 100, True))
    # }

    def search_placeholder(self):
        return "Поиск по названию и автору"


admin.add_view(BooksView(Book, db_session.create_session(), name="Книги"))

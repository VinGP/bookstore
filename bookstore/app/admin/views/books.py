from app import file_path
from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.books import Book
from flask import url_for
from flask_admin import form
from markupsafe import Markup


def name_gen_image(model, file_data):
    hash_name = (
        f'image/book/{model.generate_image_uuid()}.{file_data.filename.split(".")[-1]}'
    )
    return hash_name


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
        "image",
    ]

    column_list = (
        "id",
        "title",
        "author",
        "available_quantity",
        "price",
        "publisher",
        "image",
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
        if not model.image:
            return ""

        url = url_for("static", filename=model.image)
        return Markup(f'<img src={url} width="100">')

    column_formatters = {"image": _list_thumbnail}

    form_extra_fields = {
        "image": form.ImageUploadField(
            "",
            base_path=file_path,
            namegen=name_gen_image,
            allowed_extensions=["jpeg", "jpg", "png", "webp"],
            max_size=(1200, 780, True),
            # thumbnail_size=(100, 100, False),
        )
    }

    def search_placeholder(self):
        return "Поиск по названию и автору"

    def create_form(self, obj=None):
        return super(BooksView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(BooksView, self).edit_form(obj)


admin.add_view(BooksView(Book, db_session.create_session(), name="Книги"))

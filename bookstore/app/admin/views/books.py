from app import file_path
from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.books import Book
from app.models.images import Image, generate_image_uuid
from flask import url_for
from flask_admin import form
from flask_admin.model import InlineFormAdmin
from markupsafe import Markup


def name_gen_image(model, file_data):
    hash_name = (
        f'image/book/{generate_image_uuid()}.{file_data.filename.split(".")[-1]}'
    )
    return hash_name


class InlineModelForm(InlineFormAdmin):
    form_columns = [
        "id",
        "filename",
    ]
    form_extra_fields = {
        "filename": form.ImageUploadField(
            "",
            base_path=file_path,
            namegen=name_gen_image,
            allowed_extensions=["jpeg", "jpg", "png", "webp"],
            max_size=(1200, 780, True),
        )
    }


class BooksView(MyBaseView):
    column_display_pk = True
    column_hide_backrefs = False
    column_display_all_relations = True
    column_searchable_list = ["authors.first_name", "title", "isbn"]
    column_filters = ["authors", "publisher"]
    inline_models = (InlineModelForm(Image),)
    form_columns = [
        "isbn",
        "title",
        "authors",
        "available_quantity",
        "price",
        "publisher",
        "categories",
        "image_path",
    ]

    column_list = (
        "id",
        "title",
        "authors",
        "available_quantity",
        "price",
        "publisher",
        "image_path",
        "isbn",
        "categories",
    )
    column_labels = dict(
        id="ID",
        title="Название",
        authors="Автор",
        available_quantity="Количество экземпляров",
        publisher="Издательство",
        price="Цена",
        isbn="ISBN",
        image_path="Основная картинка",
        categories="Категория",
    )

    form_extra_fields = {
        "image_path": form.ImageUploadField(
            "",
            base_path=file_path,
            namegen=name_gen_image,
            allowed_extensions=["jpeg", "jpg", "png", "webp"],
            max_size=(1200, 780, True),
        )
    }

    def _list_thumbnail(view, context, model, name):
        if not model.image_path:
            return ""
        url = url_for("static", filename=model.image_path)
        return Markup(f'<img src={url} width="100">')

    column_formatters = {"image_path": _list_thumbnail}

    def search_placeholder(self):
        return "Поиск по названию и автору"

    def create_form(self, obj=None):
        return super(BooksView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(BooksView, self).edit_form(obj)


admin.add_view(BooksView(Book, db_session.create_session(), name="Книги"))

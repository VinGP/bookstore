from app import file_path
from app.admin import admin
from app.admin.views.base import MyBaseView
from app.models import db_session
from app.models.books import Book
from app.models.images import Image
from flask import url_for
from flask_admin import form
from flask_admin.model import InlineFormAdmin
from markupsafe import Markup


def name_gen_image(model, file_data):
    hash_name = (
        f'image/book/{model.generate_image_uuid()}.{file_data.filename.split(".")[-1]}'
    )
    return hash_name


class InlineModelForm(InlineFormAdmin):
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
    column_searchable_list = ["author.first_name", "title", "isbn"]
    column_filters = ["author", "publisher"]
    inline_models = (InlineModelForm(Image),)
    form_columns = [
        "isbn",
        "title",
        "author",
        "available_quantity",
        "price",
        "publisher",
        # "images",
    ]

    column_list = (
        "id",
        "title",
        "author",
        "available_quantity",
        "price",
        "publisher",
        "images",
        "isbn",
    )
    column_labels = dict(
        id="ID",
        title="Название",
        author="Автор",
        available_quantity="Количество экземпляров",
        publisher="Издательство",
        price="Цена",
        isbn="ISBN",
    )

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return ""

        url = url_for("static", filename=model.images[0].filename)
        return Markup(f'<img src={url} width="100">')

    column_formatters = {"images": _list_thumbnail}

    def search_placeholder(self):
        return "Поиск по названию и автору"

    def create_form(self, obj=None):
        return super(BooksView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(BooksView, self).edit_form(obj)


admin.add_view(BooksView(Book, db_session.create_session(), name="Книги"))

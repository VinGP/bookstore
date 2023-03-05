# import ast
#
# from flask import url_for
# from flask_admin.helpers import get_url
# from markupsafe import Markup
#
# from app.admin import admin
# from app.admin.views.base import MyBaseView
# from app.models import db_session
# from app.models.books import Book
# from flask_admin.form.upload import ImageUploadField
#
# import ast
# from PIL import Image
# from wtforms.widgets import html_params
# from wtforms.utils import unset_value
# from flask_admin.helpers import get_url
# from flask_admin.form.upload import ImageUploadField
# from flask_admin._compat import string_types, urljoin
#
# file_path = ""
# prefix_name = ""
#
# class MultipleImageUploadInput(object):
#     empty_template = "<input %(file)s multiple>"
#
#     # display multiple images in edit view of flask-admin
#     data_template = ("<div class='image-thumbnail'>"
#                      "   %(images)s"
#                      "</div>"
#                      "<input %(file)s multiple>")
#
#     def __call__(self, field, **kwargs):
#
#         kwargs.setdefault("id", field.id)
#         kwargs.setdefault("name", field.name)
#
#         args = {
#             "file": html_params(type="file", **kwargs),
#         }
#
#         if field.data and isinstance(field.data, string_types):
#
#             attributes = self.get_attributes(field)
#
#             args["images"] = "&emsp;".join([
#                                                "<img src='{}' /><input type='checkbox' name='{}-delete'>Delete</input>"
#                                            .format(src, filename) for src, filename in
#                                                attributes])
#
#             template = self.data_template
#
#         else:
#             template = self.empty_template
#
#         return Markup(template % args)
#
#     def get_attributes(self, field):
#
#         for item in ast.literal_eval(field.data):
#
#             filename = item
#
#             if field.thumbnail_size:
#                 filename = field.thumbnail_size(filename)
#
#             if field.url_relative_path:
#                 filename = urljoin(field.url_relative_path, filename)
#
#             yield get_url(field.endpoint, filename=filename), item
#
#
# class MultipleImageUploadField(ImageUploadField):
#     widget = MultipleImageUploadInput()
#
#     def process(self, formdata, data=unset_value):
#
#         self.formdata = formdata  # get the formdata to delete images
#         return super(MultipleImageUploadField, self).process(formdata, data)
#
#     def process_formdata(self, valuelist):
#
#         self.data = list()
#
#         for value in valuelist:
#             if self._is_uploaded_file(value):
#                 self.data.append(value)
#
#     def populate_obj(self, obj, name):
#
#         field = getattr(obj, name, None)
#
#         if field:
#
#             filenames = ast.literal_eval(field)
#
#             for filename in filenames[:]:
#                 if filename + "-delete" in self.formdata:
#                     self._delete_file(filename)
#                     filenames.remove(filename)
#         else:
#             filenames = list()
#
#         for data in self.data:
#             if self._is_uploaded_file(data):
#                 self.image = Image.open(data)
#
#                 filename = self.generate_name(obj, data)
#                 filename = self._save_file(data, filename)
#
#                 data.filename = filename
#
#                 filenames.append(filename)
#
#         setattr(obj, name, str(filenames))
#
#
# class BooksView(MyBaseView):
#     column_display_pk = True
#     column_hide_backrefs = False
#     column_display_all_relations = True
#     column_searchable_list = ["author.first_name", "title"]
#     column_filters = ["author", "publisher"]
#     form_columns = ["title", "author", "available_quantity", "price", "publisher",
#                     "images"]
#
#     column_list = (
#         "id", "title", "author", "available_quantity", "price", "publisher", "images")
#     column_labels = dict(id='ID', title="Название", author="Автор",
#                          available_quantity="Количество экземпляров",
#                          publisher="Издательство",
#                          price="Цена", )
#
#     def _list_thumbnail(view, context, model, name):
#         if not model.images:
#             return ''
#
#         def gen_img(filename):
#             return '<img src="{}">'.format(url_for('static',
#                                                    filename="images/products/" + form.thumbgen_filename(
#                                                        model.image)))
#
#         return Markup(
#             "<br />".join([gen_img(image) for image in ast.literal_eval(model.images)]))
#
#     column_formatters = {
#         'images': _list_thumbnail}  # My column name is images in this case
#
#     form_extra_fields = {'images': MultipleImageUploadField("Images",
#                                                             base_path=file_path,
#                                                             url_relative_path="images/products/",
#                                                             # relative path of your image (you need to give this in order to see thumbnail in edit secction)
#                                                             thumbnail_size=(
#                                                             200, 200, True),
#                                                             # need to pass to make thumbnail
#                                                             namegen=prefix_name)  # rename each image
#
#     def search_placeholder(self):
#         return "Поиск по названию и автору"
#
#
# admin.add_view(BooksView(Book, db_session.create_session(), name="Книги"))

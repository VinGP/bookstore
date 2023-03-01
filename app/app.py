from config import Config
from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db_session
from models.authors import Author
from models.books import Book
from models.publishers import Publisher

app = Flask(__name__)
app.config.from_object(Config)
db_session.global_init(app.config["SQLALCHEMY_DATABASE_URI"])

admin = Admin(app, name="BookStoreManager", template_mode="bootstrap4")


class BooksView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_display_all_relations = True
    column_searchable_list = ["author.first_name", "title"]
    column_filters = ["author", "publisher"]
    form_columns = ["title", "author", "available_quantity", "price", "publisher"]

    column_list = ("id", "title", "author", "available_quantity", "price", "publisher")


admin.add_view(BooksView(Book, db_session.create_session()))
admin.add_view(ModelView(Publisher, db_session.create_session()))
admin.add_view(ModelView(Author, db_session.create_session()))


@app.route("/")
def hello_world():
    return jsonify({"res": "Hello World!!!"})


@app.route("/i")
def i():
    return jsonify({"res": "i!!!"})


@app.route("/add/<n>")
def add(n):
    try:
        db_sess = db_session.create_session()
        a = Author()
        a.first_name = "test"
        a.second_name = "test"
        db_sess.add(a)
        db_sess.commit()
        at = {
            "first_name": a.first_name,
            "id": a.id,
            "second_name": a.second_name,
            "surname": a.surname,
        }

        p = Publisher()
        p.name = "test"
        db_sess.add(p)
        db_sess.commit()
        pb = {"id": p.id, "name": p.name}
        b = Book()
        b.isbn = "123423-1221-131-33"
        b.title = "test"
        b.price = 1000
        b.available_quantity = 100
        b.author_id = a.id
        b.publisher_id = p.id
        db_sess.add(b)
        db_sess.commit()
        bk = {"p": b.publisher_id, "a": a.id, "t": b.title}
        print(jsonify({"b": bk, "p": pb, "a": at}))
        return jsonify({"b": bk, "p": pb, "a": at})

    except Exception as e:
        return jsonify(e)


@app.route("/get/")
def get():
    books = Book.query.all()
    print([b.__dict__ for b in books])
    res = {}
    for book in books:
        res[book.id] = book.title
    return jsonify(res)


if __name__ == "__main__":
    app.run()

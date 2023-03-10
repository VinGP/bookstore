from app.models import db_session
from app.models.authors import Author
from app.models.books import Book
from app.models.publishers import Publisher
from flask import jsonify, render_template, request, session

from . import app, babel


@app.context_processor
def utility_processor():
    def format_author(author: Author):
        return f"{author.first_name} {author.second_name[0]}.{' ' + author.surname[0] + '.' if author.surname else ''}"

    return dict(format_author=format_author)


@babel.localeselector
def get_locale():
    if request.args.get("lang"):
        session["lang"] = request.args.get("lang")
    return session.get("lang", "ru")


@app.route("/")
def index():
    with db_session.create_session() as db_sess:
        books = db_sess.query(Book).all()
        return render_template("index.html", books=books * 2, title="Книжный магазин")


@app.route("/i")
def i():
    return jsonify({"res": "i!!!"})


@app.route("/book/<int:id>")
def book(id: int):
    with db_session.create_session() as db_sess:
        book = db_sess.query(Book).filter(Book.id == id).first()
        if book:
            res = {
                "id": book.id,
                "title": book.title,
                "author": book.author.__repr__(),
                "isbn": book.isbn,
            }
            return jsonify({"res": res})
        return jsonify({"res": {}})


@app.route("/author/<int:id>")
def author(id: int):
    with db_session.create_session() as db_sess:
        author = db_sess.query(Author).filter(Author.id == id).first()
        res = {
            "id": author.id,
            "first_name": author.first_name,
            "second_name": author.second_name,
            "surname": author.surname,
        }
    return jsonify(dict(res=res))


@app.route("/add/<n>")
def add(n):
    try:
        with db_session.create_session() as db_sess:
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
            # print(jsonify({"b": bk, "p": pb, "a": at}))
            return jsonify({"b": bk, "p": pb, "a": at})

    except Exception as e:
        return jsonify(e)


@app.route("/get/")
def get():
    books = Book.query.all()
    # print([b.__dict__ for b in books])
    res = {}
    for book in books:
        res[book.id] = book.title
    return jsonify(res)


@app.route("/mail/")
def test_mail():
    from app.mail import send_email

    send_email(
        "Заказ | BookStore",
        f"Test Book Store <{app.config['MAIL_USERNAME']}>",
        ["ivan.voronin.25@mail.ru"],
        render_template("mail/test.txt"),
        render_template("mail/test.html"),
    )
    return jsonify({"res": True})


@app.route("/personal")
def personal():
    return "personal"


@app.route("/cart")
def cart():
    return "cart"

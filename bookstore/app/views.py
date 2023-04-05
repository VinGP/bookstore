from random import randint

from app.models import db_session
from app.models.authors import Author
from app.models.books import Book
from app.models.cart import CartBook
from app.models.categories import Category, books_categories
from app.services.carts import (
    add_book_to_cart,
    delete_book_in_cart,
    get_cart_total_price,
    get_cart_weight,
    get_count_books_in_cart,
    update_count_book_in_cart,
)
from app.services.catigories import get_main_categorise
from app.services.mail import confirm_mail, send_confirm_mail
from flask import abort, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy_pagination import paginate

from . import app, babel
from .services.users import get_user_by_id


def format_weight(n: int):
    return round(n / 1000, 2)


@app.context_processor
def utility_processor():
    def format_author(author: Author):
        return f"{author.first_name} {author.second_name[0]}.{' ' + author.surname[0] + '.' if author.surname else ''}"

    def main_categorise():
        with db_session.create_session() as db_sess:
            return get_main_categorise(db_sess)

    def cart_total():
        with db_session.create_session() as db_sess:
            total = get_cart_total_price(db_sess, current_user.cart)
            return total

    def count_book_in_cart(book):
        with db_session.create_session() as db_sess:
            count = (
                db_sess.query(CartBook.count)
                .filter(
                    CartBook.book_id == book.id,
                    CartBook.cart_id == current_user.cart.id,
                )
                .first()
            )
            if count:
                return count[0]
            return 0

    # def format_number(n: int | str):
    #     import re
    #     return re.sub(r"/\B(?<!\.\d)(?=(\d{3})+(?!\d))/g", " ", str(n))

    def count_books_in_cart():
        if current_user.is_authenticated:
            with db_session.create_session() as db_sess:
                count = get_count_books_in_cart(db_sess, current_user.cart)
                return count
        return 0

    def book_in_cart(book):
        if current_user.is_authenticated:
            with db_session.create_session() as db_sess:
                book = (
                    db_sess.query(CartBook)
                    .filter(CartBook.book == book, CartBook.cart == current_user.cart)
                    .first()
                )
                if book:
                    return True
        return False

    def cart_weight():
        with db_session.create_session() as db_sess:
            weight = format_weight(get_cart_weight(db_sess, current_user.cart))
            return weight

    return dict(
        format_author=format_author,
        main_categorise=main_categorise,
        book_in_cart=book_in_cart,
        cart_total=cart_total,
        count_book_in_cart=count_book_in_cart,
        count_books_in_cart=count_books_in_cart,
        cart_weight=cart_weight,
    )


@babel.localeselector
def get_locale():
    if request.args.get("lang"):
        session["lang"] = request.args.get("lang")
    return session.get("lang", "ru")


@app.route("/")
def index():
    len_category = 10
    with db_session.create_session() as db_sess:
        """
        novelties - новинки
        best_prices - лучшие цены
        random_book - случайная книга
        editors_choice - выбор редакции
        """

        random_books = (
            db_sess.query(Book).offset(randint(100, 5000)).limit(len_category).all()
        )

        novelties = (
            db_sess.query(Book).order_by(Book.publication_date).limit(len_category)
        ).all()
        best_prices = db_sess.query(Book).order_by(Book.price).limit(len_category).all()
        editors_choice = (
            db_sess.query(Book).offset(randint(100, 5000)).limit(len_category).all()
        )
        index_books = {
            "Новинки": novelties,
            "Лучшие цены": best_prices,
            "Выбор редакции": editors_choice,
            "Cлучайная книга": random_books,
        }

        return render_template(
            "index.html",
            index_books=index_books,
            title="Книжный магазин",
        )


@app.route("/category/<int:category_id>")
def category_view(category_id):
    page = request.args.get("page", 1, type=int)
    per_page = 24

    with db_session.create_session() as db_sess:
        category = db_sess.query(Category).filter(Category.id == category_id).first()

        subcategories = Category.get_children_list(db_sess, category.id)

        # parent_categories = Category.get_parents_list(db_sess, category.id)

        books = (
            db_sess.query(Book)
            .join(books_categories)
            .join(Category)
            .filter(Category.id.in_([ct.id for ct in subcategories]))
            .order_by(Book.publication_date)
        )

        pagination = paginate(books, page, per_page)
        next_url = (
            url_for("category_view", category_id=category_id, page=pagination.next_page)
            if pagination.has_next
            else None
        )
        prev_url = (
            url_for(
                "category_view", category_id=category_id, page=pagination.previous_page
            )
            if pagination.has_previous
            else None
        )

        categories = get_main_categorise(db_sess)

        return render_template(
            "category.html",
            books=pagination.items,
            categories=categories,
            category_title=category.name,
            total_count=pagination.total,
            next_url=next_url,
            prev_url=prev_url,
            current_page=page,
            category_id=category_id,
            end_page=pagination.pages,
            title=category.name,
        )


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


@app.route("/ordering")
def ordering():
    return "ordering"


@app.route("/cart")
@login_required
def cart():
    books = sorted(
        [(cb, cb.book) for cb in current_user.cart.books], key=lambda x: x[1].title
    )

    return render_template("cart.html", books=books, title="Корзина")


# login_required
@app.route("/add", methods=["POST"])
def add_to_cart():
    data = request.json
    if current_user.is_authenticated:
        with db_session.create_session() as db_sess:
            book = db_sess.query(Book).filter(Book.id == data["id"]).first()

            add_book_to_cart(session=db_sess, cart=current_user.cart, book=book)

            return jsonify(dict(msg=True, id=book.id, success=True))
    return jsonify(dict(success=False, redirect=url_for("register")))


@app.route("/delete_cart_book", methods=["POST"])
def delete_cart_book():
    data = request.json
    if current_user.is_authenticated:
        with db_session.create_session() as db_sess:
            book = db_sess.query(Book).filter(Book.id == data["id"]).first()
            delete_book_in_cart(session=db_sess, cart=current_user.cart, book=book)
            total_cart_price = get_cart_total_price(db_sess, current_user.cart)
            count_books_in_cart = get_count_books_in_cart(db_sess, current_user.cart)
            cart_weight = format_weight(get_cart_weight(db_sess, current_user.cart))
            return jsonify(
                dict(
                    msg=True,
                    id=book.id,
                    success=True,
                    total_cart_price=total_cart_price,
                    count_books_in_cart=count_books_in_cart,
                    cart_weight=cart_weight,
                )
            )
    return jsonify(dict(success=False, redirect=url_for("register")))


@app.route("/update_count_book_in_cart", methods=["POST"])
def update_count_book_in_cart_view():
    if current_user.is_authenticated:
        data = request.json
        with db_session.create_session() as db_sess:
            book = db_sess.query(Book).filter(Book.id == data["id"]).first()
            cart_item = update_count_book_in_cart(
                db_sess, book=book, cart=current_user.cart, count=data["count"]
            )
            total_price_book = cart_item.count * cart_item.book.price
            total_cart_price = get_cart_total_price(db_sess, current_user.cart)
            count_books_in_cart = get_count_books_in_cart(db_sess, current_user.cart)
            cart_weight = format_weight(get_cart_weight(db_sess, current_user.cart))
            return jsonify(
                success=True,
                id=data["id"],
                count=cart_item.count,
                total_price_book=total_price_book,
                total_cart_price=total_cart_price,
                count_books_in_cart=count_books_in_cart,
                cart_weight=cart_weight,
            )
    return jsonify(dict(success=False, redirect=url_for("register")))


@app.route("/get_count_books_in_cart", methods=["POST"])
def get_count_books_in_cart_view():
    if current_user.is_authenticated:
        with db_session.create_session() as db_sess:
            count = get_count_books_in_cart(db_sess, current_user.cart)
            return jsonify(dict(success=True, count=count))
    return jsonify(dict(success=True, count=0))


@app.route("/unconfirmed_mail/<int:id>")
def unconfirmed_mail(id):
    with db_session.create_session() as db_sess:
        user = get_user_by_id(db_sess, id)
        if user and not user.email_confirmed:
            return render_template(
                "mail/unconfirmed_mail.html",
                title="Проверьте свою электронную почту",
                email=user.email,
                id=id,
                recent_mail_button=True,
            )
    return redirect(url_for("index"))


@app.route("/recent_confirm_mail/<int:id>")
def recent_confirm_mail(id):
    with db_session.create_session() as db_sess:
        user = get_user_by_id(db_sess, id)
        if user and not user.email_confirmed:
            send_confirm_mail(user)
            return render_template(
                "mail/unconfirmed_mail.html",
                title="Проверьте свою электронную почту",
                email=user.email,
                id=id,
                recent_mail_button=False,
            )
    return redirect(url_for("index"))


@app.route("/t")
def t():
    abort(404)
    return url_for("unconfirmed_mail", email="123")


@app.route("/confirm_mail/<token>")
def confirm_mail_view(token):
    email = confirm_mail(token)
    if email:
        return render_template(
            "mail/success_confirm_mail.html", title="Почта подтверждена", email=email
        )
    abort(404)

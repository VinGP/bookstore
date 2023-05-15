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
from flask import (
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy_pagination import paginate

from . import app, babel
from .forms.search import SearchForm
from .forms.user import OrderForm, UserForm
from .models.orders import DeliveryMethod, Order, OrderPayment, OrderStateName
from .services.orders import create_order
from .services.payments import confirm_payment, create_payment
from .services.publishers import get_publisher_by_id
from .services.series import get_series_by_id
from .services.users import get_user_by_id


def page_url_maker(endpoint, **kwargs):
    def wrapper(page):
        return url_for(endpoint=endpoint, **kwargs, page=page)

    return wrapper


def format_weight(n: int):
    return round(n / 1000, 2)


@app.context_processor
def utility_processor():  # noqa
    search_form = SearchForm()

    def format_author(author: Author):
        return f"{author.first_name} {author.second_name[0]}.{' ' + author.surname[0] + '.' if author.surname else ''}"

    def get_authors_books(authors):
        res = []
        for author in authors:
            res += author.books[:10]
        if len(res) > 1:
            return res[:15]
        return None

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

    def order_state_to_text(order_state):
        if isinstance(order_state, str):
            return OrderStateName[order_state].value
        else:
            return OrderStateName[order_state.name].value

    def format_date(date):
        return date.strftime("%Y-%m-%d %H:%M")

    def get_delivery_method_price(method):

        return DeliveryMethod(method.data).value[1]

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

    def get_dadata_token():
        return app.config["DADATA_API_KEY"]

    return dict(
        format_author=format_author,
        main_categorise=main_categorise,
        book_in_cart=book_in_cart,
        cart_total=cart_total,
        count_book_in_cart=count_book_in_cart,
        count_books_in_cart=count_books_in_cart,
        cart_weight=cart_weight,
        get_authors_books=get_authors_books,
        search_form=search_form,
        get_delivery_method_price=get_delivery_method_price,
        order_state_to_text=order_state_to_text,
        format_date=format_date,
        get_dadata_token=get_dadata_token,
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

    with db_session.create_session() as db_sess:
        category = db_sess.query(Category).filter(Category.id == category_id).first()

        subcategories = Category.get_children_list(db_sess, category.id)

        books = (
            db_sess.query(Book)
            .join(books_categories)
            .join(Category)
            .filter(Category.id.in_([ct.id for ct in subcategories]))
            .order_by(Book.publication_date)
        )

        pagination = paginate(books, page, app.config["PER_PAGE"])
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
            page_url_maker=page_url_maker("category_view", category_id=category_id),
        )


@app.route("/book/<int:id>")
def book(id):
    with db_session.create_session() as db_sess:
        book = db_sess.query(Book).filter(Book.id == id).first()
        if not book:
            abort(404)
            return
        if book.categories:
            parent_categories = Category.get_parents_list(
                db_sess, book.categories[0].id
            )[::-1]
        else:
            parent_categories = []
        return render_template(
            "book.html",
            book=book,
            title=book.title,
            parent_categories=parent_categories,
        )


@app.route("/publisher/<int:id>")
def publisher(id):
    page = request.args.get("page", 1, type=int)
    per_page = app.config["PER_PAGE"]
    with db_session.create_session() as db_sess:
        publisher = get_publisher_by_id(db_sess, id)
        books = db_sess.query(Book).filter(Book.publisher_id == publisher.id)
        total_count = books.count()
        pg = paginate(books, page, per_page)
        books = pg.items
        page_url_maker_publisher = page_url_maker("publisher", id=publisher.id)

        end_page = total_count // per_page + bool(total_count % per_page)

        next_page = page + 1 if end_page > page else None

        next_url = page_url_maker_publisher(next_page) if next_page else None
        prev_url = page_url_maker_publisher(page - 1) if page > 1 else None
        res = render_template(
            "publisher.html",
            books=books,
            publisher=publisher,
            total_count=total_count,
            next_url=next_url,
            prev_url=prev_url,
            current_page=page,
            end_page=end_page,
            title=str(publisher),
            page_url_maker=page_url_maker_publisher,
        )
        return res


@app.route("/series/<int:id>")
def series(id):
    with db_session.create_session() as db_sess:
        page = request.args.get("page", 1, type=int)
        per_page = app.config["PER_PAGE"]
        series = get_series_by_id(db_sess, id)
        books = series.books
        total_count = len(books)

        page_url_maker_series = page_url_maker("series", id=series.id)

        end_page = total_count // per_page + bool(total_count % per_page)

        next_page = page + 1 if end_page > page else None

        next_url = page_url_maker_series(next_page) if next_page else None
        prev_url = page_url_maker_series(page - 1) if page > 1 else None
        res = render_template(
            "series.html",
            books=books,
            series=series,
            publisher=series.publisher,
            total_count=total_count,
            next_url=next_url,
            prev_url=prev_url,
            current_page=page,
            end_page=end_page,
            title=str(series),
            page_url_maker=page_url_maker_series,
        )
        return res


@app.route("/author/<int:id>")
def author(id: int):
    page = request.args.get("page", 1, type=int)
    per_page = app.config["PER_PAGE"]
    with db_session.create_session() as db_sess:
        author = db_sess.query(Author).filter(Author.id == id).first()
        books = author.books

        total_count = len(books)

        page_url_maker_author = page_url_maker("author", id=author.id)

        end_page = total_count // per_page + bool(total_count % per_page)

        next_page = page + 1 if end_page > page else None

        next_url = page_url_maker_author(next_page) if next_page else None
        prev_url = page_url_maker_author(page - 1) if page > 1 else None

    return render_template(
        "author.html",
        books=books,
        author=author,
        total_count=total_count,
        next_url=next_url,
        prev_url=prev_url,
        current_page=page,
        end_page=end_page,
        title=str(author),
        page_url_maker=page_url_maker_author,
    )


@app.route("/personal", methods=["POST", "GET"])
@login_required
def personal():
    form = UserForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            user = get_user_by_id(db_sess, current_user.id)
            user.name = form.name.data
            user.surname = form.surname.data
            user.phone_number = (
                form.phone_number.data if form.phone_number.data.strip() else None
            )
            db_sess.add(user)
            db_sess.commit()
        flash("Данные изменены", "success")
    else:
        form.name.data = current_user.name
        form.phone_number.data = current_user.phone_number
        form.surname.data = current_user.surname
    form.email.data = current_user.email

    return render_template("profile.html", title="Профиль", form=form)


@app.route("/orders")
@login_required
def orders():
    with db_session.create_session() as db_sess:
        orders = (
            db_sess.query(Order)
            .filter(Order.user_id == current_user.id)
            .order_by(Order.creation_date.desc())
            .all()
        )
        return render_template("orders.html", title="Заказы", orders=orders)


@app.route("/order/<int:order_id>")
@login_required
def order(order_id):
    with db_session.create_session() as db_sess:
        order = (
            db_sess.query(Order)
            .filter(Order.user_id == current_user.id, Order.id == order_id)
            .first()
        )

        if order:
            return render_template(
                "order_details.html", order=order, title=f"Заказ №{order_id}"
            )
        return abort(404)


@app.route("/api/pay/notifications", methods=["POST"])
def confirm_pay():
    if request.json["event"] == "payment.succeeded":
        payment_id = request.json["object"]["id"]
        with db_session.create_session() as db_sess:
            confirm_payment(db_sess, payment_id)
    return "Success", 200


@app.route("/ordering", methods=["POST", "GET"])
@login_required
def ordering():
    form = OrderForm()

    delivery_price = DeliveryMethod[form.delivery_method.default].value[1]
    if not current_user.cart.books:
        abort(404)
    if form.validate_on_submit():

        with db_session.create_session() as db_sess:

            order = create_order(
                db_sess,
                current_user,
                email=current_user.email,
                name=form.name.data,
                surname=form.surname.data,
                patronymic=form.patronymic.data,
                phone_number=form.phone_number.data,
                delivery_price=DeliveryMethod[form.delivery_method.data].value[1],
                delivery_method=DeliveryMethod[form.delivery_method.data],
                region=form.region.data,
                street=form.street.data,
                city=form.city.data,
                house=form.house.data,
                flat=form.flat.data,
                postcode=form.postal_code.data,
                comment=form.order_comment.data,
            )

            confirmation_url = create_payment(
                session=db_sess,
                order_id=order.id,
                amount=order.get_order_sum(),
                description=f"Заказ №{order.id}",
                return_url=url_for("order", order_id=order.id, _external=True),
            )

            if confirmation_url:
                return redirect(confirmation_url)
            return redirect(url_for("order", order_id=order.id))

    form.name.data = current_user.name
    form.surname.data = current_user.surname
    form.email.data = current_user.email
    form.phone_number.data = (
        current_user.phone_number if current_user.phone_number else None
    )
    with db_session.create_session() as db_sess:
        total_products_price = get_cart_total_price(db_sess, current_user.cart)
        count_books_in_order = get_count_books_in_cart(db_sess, current_user.cart)
        order_weight = format_weight(get_cart_weight(db_sess, current_user.cart))
        total_order_price = total_products_price + delivery_price

    return render_template(
        "ordering.html",
        form=form,
        title="Оформление заказа",
        total_products_price=total_products_price,
        count_books_in_order=count_books_in_order,
        order_weight=order_weight,
        total_order_price=total_order_price,
        delivery_price=delivery_price,
    )


@app.route("/cart")
@login_required
def cart():
    books = sorted(
        [(cb, cb.book) for cb in current_user.cart.books], key=lambda x: x[1].title
    )

    return render_template("cart.html", books=books, title="Корзина")


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


@app.route("/confirm_mail/<token>")
def confirm_mail_view(token):
    email = confirm_mail(token)
    if email:
        return render_template(
            "mail/success_confirm_mail.html", title="Почта подтверждена", email=email
        )
    abort(404)


@app.route("/search")
def search():
    q = request.args.get("q", None)
    page = request.args.get("page", 1, type=int)
    per_page = app.config["PER_PAGE"]
    if q := q.strip():
        books, total = Book.search(q, page, per_page)

        url_maker = page_url_maker("search", q=q)

        end_page = total // per_page + bool(total % per_page)

        next_page = page + 1 if end_page > page else None

        next_url = url_maker(next_page) if next_page else None
        prev_url = url_maker(page - 1) if page > 1 else None

        return render_template(
            "search.html",
            books=books,
            total_count=total,
            next_url=next_url,
            prev_url=prev_url,
            current_page=page,
            end_page=end_page,
            title=f"Поиск: {q}",
            page_url_maker=url_maker,
            q=q,
        )

    return render_template(
        "search.html",
        books=[],
        title=f"Поиск: {q}",
        q=q,
    )


@app.route("/autocomplete/<q>")
def autocomplete(q=None):
    res = []
    if q:
        res = Book.autocomplete(q, 1, 10)
    return jsonify({"data": res})

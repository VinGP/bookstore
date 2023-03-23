from random import randint

from app import app
from app.models.db_session import create_session
from app.services.authors import create_author
from app.services.books import create_book
from app.services.catigories import add_sub_category, create_category
from app.services.images import create_image
from app.services.publishers import create_publisher
from app.services.series import create_series
from flask.cli import FlaskGroup

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    pass


@cli.command("insert_db_data")
def insert_db_data():
    from json import loads

    books_data = loads(open("books.json", "r", encoding="utf-8").read())
    for book in books_data:
        try:
            authors = book["authors"]
            title = book["title"]
            print(title)
            annotation = book["annotation"]
            image_path = book["images"]["main_image"]
            other_image = book["images"]["other_image"]
            publisher = book["publisher"]
            series = book.get("series", None)
            year = book.get("year", None)
            isbn = book["ISBN"]
            number_of_pages = book.get("number_of_pages", 3)
            size = book.get("size", None)
            weight = book.get("weight", None)
            category = book["catygory"]
            if "Подарочные" in category:
                continue
            price = randint(100, 2000)
            with create_session() as db_sess:
                book = create_book(
                    session=db_sess,
                    title=title,
                    isbn=isbn,
                    annotation=annotation,
                    price=price,
                    publisher=create_publisher(publisher),
                    authors=[create_author(db_sess, *a.split(" ")) for a in authors],
                    number_of_pages=number_of_pages,
                    size=size,
                    weight=weight,
                    year=year,
                    image_path="image/book/" + image_path,
                    available_quantity=randint(100, 1000),
                )

                if series:
                    book.series.append(create_series(db_sess, series, book.publisher))
                if other_image:
                    for img in other_image:
                        b_i = create_image(db_sess, img, book_id=book.id)
                        book.other_images.append(b_i)
                ca = None
                for c in category.split("|")[2:]:
                    if ca:
                        nc = create_category(db_sess, c)
                        add_sub_category(db_sess, ca, nc)
                        ca = nc
                    else:
                        ca = create_category(db_sess, c)
                book.categories.append(ca)
                db_sess.commit()
        except Exception as e:
            print(e)


@cli.command("delete_db_data")
def delete_db_data():
    from app.models.authors import Author, books_authors
    from app.models.books import Book
    from app.models.categories import Category, books_categories
    from app.models.images import Image
    from app.models.series import Series, books_series

    with create_session() as db_sess:
        db_sess.query(Image).delete()
        db_sess.query(books_categories).delete()
        db_sess.query(Category).delete()
        db_sess.query(books_authors).delete()
        db_sess.query(Author).delete()

        db_sess.query(books_series).delete()
        db_sess.query(Series).delete()

        db_sess.query(Book).delete()
        db_sess.commit()


if __name__ == "__main__":
    cli()

# Создание копии базы данных из которой можно будет создать базу:
# pg_dump -U hello_flask -p 54320 -d hello_flask_dev  -f ./d.sql
# Запуск: python manage.py --env-file .env.dev run -h 0.0.0.0

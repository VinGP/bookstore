import os

import sqlalchemy
from app import file_path
from app.models.mixins import SearchableMixin
from sqlalchemy import event, orm
from sqlalchemy.event import listens_for

from ..search import add_to_index, remove_from_index
from .authors import Author
from .db_session import SqlAlchemyBase
from .publishers import Publisher


class Book(SearchableMixin, SqlAlchemyBase):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    isbn = sqlalchemy.Column(sqlalchemy.String(128), unique=True)
    title = sqlalchemy.Column(sqlalchemy.String(255))
    annotation = sqlalchemy.Column(sqlalchemy.Text())
    publication_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )
    available_quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    publisher_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("publishers.id"), nullable=False
    )
    publisher = orm.relationship("Publisher")

    other_images = orm.relationship("Image", backref="books", cascade="all,delete")

    categories = orm.relationship(
        "Category", secondary="books_categories", backref="books"
    )

    authors = orm.relationship("Author", secondary="books_authors", lazy="selectin")

    year = sqlalchemy.Column(sqlalchemy.Integer)
    number_of_pages = sqlalchemy.Column(sqlalchemy.Integer)
    size = sqlalchemy.Column(sqlalchemy.String(128), default="0 x 0 x 0")
    weight = sqlalchemy.Column(sqlalchemy.Integer)  # вес

    image_path = sqlalchemy.Column(sqlalchemy.String(250), nullable=True)

    series = orm.relationship("Series", secondary="books_series")

    def get_payload(self):
        payload = {}
        payload["isbn"] = self.isbn
        payload["title"] = self.title
        # payload["annotation"] = self.annotation
        payload["publisher"] = self.publisher.name
        payload["series"] = [s.name for s in self.series]
        payload["authors"] = [str(a) for a in self.authors]
        return payload


@listens_for(Book, "after_delete")
def del_image(mapper, connection, target):
    if target.image_path:
        try:
            os.remove(os.path.join(file_path, target.image_path))
        except OSError:
            pass


@event.listens_for(Publisher, "after_update")
def update_publisher(mapper, session, instance):
    for book in instance.books:
        add_to_index(book.__tablename__, book)


@event.listens_for(Author, "after_update")
def update_author(mapper, session, instance):
    for book in instance.books:
        add_to_index(book.__tablename__, book)


@event.listens_for(Book, "after_update")
def update_book(m, session, instance):
    print(m, session, instance)
    add_to_index(instance.__tablename__, instance)


@event.listens_for(Book, "after_insert")
def add_book_to_index(mapper, session, instance):
    add_to_index(instance.__tablename__, instance)


@event.listens_for(Book, "after_delete")
def after_delete_book(mapper, session, instance):
    try:
        remove_from_index(instance.__tablename__, instance)
    except Exception as e:
        print(e)

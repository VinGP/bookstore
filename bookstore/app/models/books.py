import os

import sqlalchemy
from app import file_path
from sqlalchemy import orm
from sqlalchemy.event import listens_for

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
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


@listens_for(Book, "after_delete")
def del_image(mapper, connection, target):
    if target.image_path:
        try:
            os.remove(os.path.join(file_path, target.image_path))
        except OSError:
            pass

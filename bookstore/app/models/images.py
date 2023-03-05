import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

books_images = sqlalchemy.Table(
    "books_images",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("book_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column(
        "image_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("images.id")
    ),
)


class Image(SqlAlchemyBase):
    __tablename__ = "images"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    path = sqlalchemy.Column(sqlalchemy.String(128), default="1234")

    def __repr__(self):
        return self.path

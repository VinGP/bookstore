import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Author(SqlAlchemyBase):
    __tablename__ = "authors"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    second_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(128))

    books = orm.relationship("Book", secondary="books_authors", lazy="select")

    def __repr__(self):
        return f"{self.first_name} {self.second_name}{' ' + self.surname if self.surname else ''}"

    def __str__(self):
        return f"{self.first_name} {self.second_name}{' ' + self.surname if self.surname else ''}"


books_authors = sqlalchemy.Table(
    "books_authors",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("books", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column(
        "authors", sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id")
    ),
)

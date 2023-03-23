import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Series(SqlAlchemyBase):
    __tablename__ = "series"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256))
    publisher_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("publishers.id"), nullable=False
    )
    publisher = orm.relationship("Publisher")
    books = orm.relationship(
        "Book",
        secondary="books_series",
    )

    def __repr__(self):
        return self.name


books_series = sqlalchemy.Table(
    "books_series",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("books", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column("series", sqlalchemy.Integer, sqlalchemy.ForeignKey("series.id")),
)

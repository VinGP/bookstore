import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    isbn = sqlalchemy.Column(sqlalchemy.String(128))
    title = sqlalchemy.Column(sqlalchemy.String(255))
    publication_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )
    available_quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id"), nullable=False
    )
    author = orm.relationship("Author")
    publisher_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("publishers.id"), nullable=False
    )
    publisher = orm.relationship("Publisher")

    images = orm.relationship("Image")

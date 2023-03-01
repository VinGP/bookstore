import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Publisher(SqlAlchemyBase):
    __tablename__ = "publishers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(128))
    books = orm.relationship("Book")

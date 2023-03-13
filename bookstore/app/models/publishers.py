import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Publisher(SqlAlchemyBase):
    __tablename__ = "publishers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(256))
    address = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String(256), nullable=True)
    books = orm.relationship("Book")

    def __repr__(self):
        return self.name

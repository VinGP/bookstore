import sqlalchemy
from db_session import SqlAlchemyBase
from sqlalchemy import orm


class Author(SqlAlchemyBase):
    __tablename__ = "authors"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    first_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    second_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(128))
    books = orm.relationship("Book", back_populates="author")

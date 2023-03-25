import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    __tablename__ = "carts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    )

    books = orm.relationship(
        "CartBook", lazy="subquery", back_populates="cart", cascade="all"
    )

    user = orm.relationship("User", back_populates="cart")


class CartBook(SqlAlchemyBase):
    __tablename__ = "carts_books"

    cart_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("carts.id"),
        primary_key=True,
    )
    book_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("books.id"),
        primary_key=True,
    )
    book = orm.relationship("Book", lazy="subquery", backref="carts")
    count = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    cart = orm.relationship("Cart", back_populates="books")

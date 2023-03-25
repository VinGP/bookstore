import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = "orders"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )
    completion_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    products = orm.relationship("OrderProduct")
    state = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("orders_states.id"), nullable=False
    )


class OrderState(SqlAlchemyBase):
    __tablename__ = "orders_states"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)


class OrderProduct(SqlAlchemyBase):
    __tablename__ = "order_product"
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("orders.id"), nullable=False
    )
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id"), nullable=False
    )
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


class DeliveryMethod(SqlAlchemyBase):
    __tablename__ = "delivery_methods"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


class Payment(SqlAlchemyBase):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

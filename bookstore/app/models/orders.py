import enum

import sqlalchemy
from sqlalchemy import Enum, event, orm

from .db_session import SqlAlchemyBase


class OrderState(enum.Enum):
    CREATED = 1  # создан
    CONFIRMED = 2  # подтвержден
    COLLECTED = 3  # собран
    IN_DELIVERY = 4  # в доставке
    DELIVERED = 5  # доставлен


class OrderStateName(enum.Enum):
    CREATED = "Создан"
    CONFIRMED = "Подтвержден"
    COLLECTED = "Собран"
    IN_DELIVERY = "В доставке"
    DELIVERED = "Доставлен"


class DeliveryMethod(enum.Enum):
    POST = ("Почта России", 350)
    CDEK = ("СДЕК", 500)
    POST5 = ("5POST", 250)

    @classmethod
    def choices(cls):
        return [
            (choice, f"{choice.value[0]} - {choice.value[1]} руб") for choice in cls
        ]

    @classmethod
    def coerce(cls, item):
        print(item, type(item))
        res = cls(int(item)) if not isinstance(item, cls) else item
        print("coerce", type(res))
        return res

    def __str__(self):
        return str(self.name)


class OrderPersonalData(SqlAlchemyBase):
    __tablename__ = "orders_personals_data"
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("orders.id"),
        nullable=False,
        primary_key=True,
    )

    order = orm.relationship("Order", back_populates="personal_data", uselist=False)

    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)


class OrderDelivery(SqlAlchemyBase):
    __tablename__ = "orders_deliveries"
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("orders.id"),
        nullable=False,
        primary_key=True,
    )
    order = orm.relationship("Order", back_populates="delivery", cascade="all,delete")
    delivery_method = sqlalchemy.Column(
        Enum(DeliveryMethod), default=DeliveryMethod.POST
    )
    delivery_price = sqlalchemy.Column(sqlalchemy.Integer(), nullable=False)
    city = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    house = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    flat = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    postcode = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    region = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    street = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)


class Order(SqlAlchemyBase):
    __tablename__ = "orders"

    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False
    )
    user = orm.relationship(
        "User", backref="orders", lazy="subquery", cascade="all,delete"
    )
    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )
    completion_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    products = orm.relationship("OrderProduct", cascade="all, delete-orphan")

    state = sqlalchemy.Column(Enum(OrderState), default=OrderState.CREATED)

    order_states = orm.relationship("OrdersStates", cascade="all, delete-orphan")

    comment = sqlalchemy.Column(sqlalchemy.Text(), nullable=True)
    personal_data = orm.relationship(
        "OrderPersonalData", uselist=False, cascade="all, delete-orphan"
    )
    delivery = orm.relationship(
        "OrderDelivery", uselist=False, cascade="all, delete-orphan"
    )

    payment = orm.relationship(
        "OrderPayment", uselist=False, cascade="all, delete-orphan"
    )

    def set_state(self, new_state: OrderState):
        if (
            self.state
            and self.state != new_state
            and self.state.value + 1 != new_state.value
        ):
            for i in range(self.state.value + 1, new_state.value + 1):
                self.state = OrderState(i)
                ord_st = OrdersStates()
                ord_st.order_id = self.id
                ord_st.state = self.state
                self.order_states.append(ord_st)
        else:
            self.state = new_state
            ord_st = OrdersStates()
            ord_st.order_id = self.id
            ord_st.state = self.state
            self.order_states.append(ord_st)

    def get_order_sum(self):
        summa = 0
        for product in self.products:
            summa += product.price * product.quantity
        summa += self.delivery.delivery_price

        return summa


@event.listens_for(Order, "after_update")
def update_book(m, session, instance):
    from app.services.orders import send_order_status_mail

    send_order_status_mail(instance)


class OrdersStates(SqlAlchemyBase):
    __tablename__ = "orders_states"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True
    )
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("orders.id"), nullable=False
    )
    state = sqlalchemy.Column(Enum(OrderState))
    date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )


class OrderProduct(SqlAlchemyBase):
    __tablename__ = "order_product"
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("orders.id"),
        nullable=False,
        primary_key=True,
    )
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("books.id"),
        nullable=False,
        primary_key=True,
    )
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    # order = orm.relationship("Order")
    book = orm.relationship("Book")


class OrderPayment(SqlAlchemyBase):
    __tablename__ = "orders_payments"
    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True
    )

    order_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("orders.id"),
        nullable=False,
        primary_key=True,
    )

    payment_id = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    idempotency_key = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    confirmed = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    amount = sqlalchemy.Column(sqlalchemy.Float, nullable=False)

    creation_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )

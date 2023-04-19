from app import app
from app.mail import send_email
from app.models.orders import (
    Order,
    OrderDelivery,
    OrderPersonalData,
    OrderProduct,
    OrderState,
)
from flask import render_template


def create_order(
    session,
    user,
    email,
    name,
    surname,
    patronymic,
    phone_number,
    delivery_price,
    delivery_method,
    city,
    region,
    street,
    house,
    flat,
    postcode,
    comment,
):
    order = Order()
    order.user_id = user.id

    for cart_book in user.cart.books:
        order_product = OrderProduct()
        order_product.product_id = cart_book.book_id
        order_product.price = cart_book.book.price
        order_product.quantity = cart_book.count
        order.products.append(order_product)
        session.add(order_product)
        cart_book.book.available_quantity -= 1
        session.delete(cart_book)

    order.comment = comment

    order.set_state(new_state=OrderState.CREATED)
    order.delivery = OrderDelivery(
        delivery_method=delivery_method,
        region=region,
        city=city,
        street=street,
        house=house,
        flat=flat,
        postcode=postcode,
        delivery_price=delivery_price,
    )
    order.personal_data = OrderPersonalData(
        email=email,
        name=name,
        surname=surname,
        patronymic=patronymic,
        phone_number=phone_number,
    )
    session.add(order)
    session.commit()
    send_order_status_mail(order)
    return order


def send_order_status_mail(order):
    html = render_template("mail/order_details.html", order=order)
    txt = html
    subject = "Статус заказа изменён"
    send_email(
        subject,
        f"Book Store <{app.config['MAIL_USERNAME']}>",
        [order.user.email],
        txt,
        html,
    )

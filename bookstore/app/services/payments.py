import uuid

from app.models.orders import OrderPayment
from yookassa import Configuration, Payment


def save_payment(session, order_id, payment_id, idempotency_key, amount):
    order_payment = OrderPayment()
    order_payment.payment_id = payment_id
    order_payment.order_id = order_id
    order_payment.idempotency_key = idempotency_key
    order_payment.amount = amount
    session.add(order_payment)
    session.commit()
    return order_payment


def create_payment(session, order_id, amount: float, description: str, return_url: str):
    if Configuration.account_id and Configuration.secret_key:
        payment, idempotency_key = create_yookassa_payment(
            amount, description, return_url
        )
        payment_id = payment.id
        confirmation_url = payment.confirmation.confirmation_url
        save_payment(session, order_id, payment_id, idempotency_key, amount)
        return confirmation_url
    return None


def create_yookassa_payment(amount: float, description: str, return_url: str):
    idempotency_key = uuid.uuid4()
    payment = Payment.create(
        {
            "amount": {"value": amount, "currency": "RUB"},
            "confirmation": {"type": "redirect", "return_url": return_url},
            "capture": True,
            "description": description,
        },
        idempotency_key,
    )

    return payment, str(idempotency_key)


def confirm_payment(session, payment_id):
    order_payment = (
        session.query(OrderPayment)
        .filter(OrderPayment.payment_id == payment_id)
        .first()
    )
    order_payment.confirmed = True
    session.commit()

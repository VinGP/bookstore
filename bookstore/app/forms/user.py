from app.models.orders import DeliveryMethod
from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    RadioField,
    StringField,
    SubmitField,
    TelField,
    TextAreaField,
)
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    email = EmailField("Электронная почта", render_kw={"disabled": ""})
    phone_number = StringField("Номер телефона")
    submit = SubmitField("Сохранить изменения")


class OrderForm(FlaskForm):
    # ПЕРСОНАЛЬНЫЕ ДАННЫЕ
    name = StringField("Имя", validators=[DataRequired()])
    surname = StringField("Фамилия", validators=[DataRequired()])
    patronymic = StringField("Отчество", validators=[DataRequired()])

    email = EmailField("Электронная почта", render_kw={"disabled": ""})
    phone_number = TelField("Телефон", validators=[DataRequired()])

    # Доставка
    region = StringField("Регион", validators=[DataRequired()])
    city = StringField("Город", validators=[DataRequired()])
    street = StringField("Улица", validators=[DataRequired()])
    house = StringField("Дом", validators=[DataRequired()])
    flat = StringField("Квартира")

    postal_code = StringField("Почтовый индекс", validators=[DataRequired()])

    delivery_method = RadioField(
        "Способ доставки",
        choices=DeliveryMethod.choices(),
        validators=[DataRequired()],
        default=str(DeliveryMethod.POST),
    )

    payment_method = RadioField(
        "Способ оплаты",
        choices=[
            (
                "yoomoney",
                "Оплата онлайн - банковская карта, ЮMoney, SberPay (Юкасса API)",
            ),
        ],
        default="yoomoney",
    )

    order_comment = TextAreaField("Комментарий к заказу")  # Комментарий

    submit = SubmitField("Подтвердить и оплатить")

import jwt
from app import app
from app.mail import send_email
from app.models.db_session import create_session
from app.services.users import user_confirm_email
from flask import render_template, url_for


def generate_confirmation_token(email: str):
    token = jwt.encode({"email": email}, app.config["SECRET_KEY"], algorithm="HS256")
    return token


def verify_token(token):
    try:
        data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return data
    except jwt.exceptions.InvalidSignatureError:
        return None


def send_confirm_mail(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for("confirm_mail_view", token=token, _external=True)
    html = render_template("mail/confirm_mail.html", confirm_url=confirm_url)
    txt = render_template("mail/confirm_mail.txt")
    subject = "Пожалуйста подтвердите свою почту"
    send_email(
        subject,
        f"Book Store <{app.config['MAIL_USERNAME']}>",
        [user.email],
        txt,
        html,
    )


def confirm_mail(token):
    data = verify_token(token=token)
    if data:
        email = data["email"]
        with create_session() as db_sess:
            user_confirm_email(db_sess, email)
            return data["email"]
    return None

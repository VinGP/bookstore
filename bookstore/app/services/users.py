from app.models.cart import Cart
from app.models.users import User


def create_user(
    session,
    name,
    surname,
    email,
    password,
    phone_number=None,
    email_confirmed=False,
    is_admin=False,
):
    user = User()
    user.name = name
    user.surname = surname
    user.email = email
    user.set_password(password)
    user.phone_number = phone_number
    user.email_confirmed = email_confirmed
    user.is_admin = is_admin
    user.cart = Cart()

    session.add(user)
    session.commit()

    return user


def get_user_by_id(session, id: int):
    return session.query(User).get(id)


def user_exists(session, email: str):
    if session.query(User).filter(User.email == email).first():
        return True
    return False


def user_confirm_email(session, email):
    user = session.query(User).filter(User.email == email).first()
    user.email_confirmed = True
    session.commit()
    return user

from app import app, login_manager
from app.forms.auth import LoginForm, RegisterForm
from app.models import db_session
from app.models.users import User
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as db_sess:
        return db_sess.query(User).get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("login")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get("next") or url_for("index"))
        flash("Неправильный логин или пароль")
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("auth/login.html", title="Авторизация", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        with db_session.create_session() as db_sess:
            if db_sess.query(User).filter(User.email == form.email.data).first():
                flash("Такой пользователь уже есть")
            else:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                    surname=form.surname.data,
                )
                user.set_password(form.password.data)
                db_sess.add(user)
                db_sess.commit()
                login_user(user, remember=form.remember_me.data)
    if current_user.is_authenticated:
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("auth/register.html", title="Регистрация", form=form)

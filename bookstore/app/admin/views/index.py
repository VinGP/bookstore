from app.admin.forms.auth import RegisterForm

# from app import admin
# from app.admin.views.books import BooksView
from app.forms.auth import LoginForm
from app.models import db_session

# from app.models.authors import Author
# from app.models.books import Book
from app.models.users import User
from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_login import current_user, login_user, logout_user

# from app.models.publishers import Publisher
# from flask_admin.contrib.sqla import ModelView


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(".login_view", next=request.url))
        return super(MyAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        # handle user login
        # form = LoginForm(request.form)
        # if form.validate_on_submit():
        #     db_sess = db_session.create_session()
        #     user = db_sess.query(User).filter(User.email == form.email.data).first()
        #     if user and user.check_password(form.password.data):
        #         login_user(user, remember=form.remember_me.data)

        if current_user.is_authenticated:
            return redirect(url_for(".index"))
        return redirect(url_for("login", next=request.url))
        # link = '<p>Don\'t have an account? <a href="' + url_for(
        #     '.register_view') + '">Click here to register.</a></p>'
        # self._template_args['form'] = form
        # self._template_args['link'] = link
        # return super(MyAdminIndexView, self).index()

    @expose("/register/", methods=("GET", "POST"))
    def register_view(self):
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            user = User()

            # form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = User.generate_password_hash(form.password.data)

            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()

            login_user(user)
            return redirect(url_for(".index"))
        link = (
            '<p>Already have an account? <a href="'
            + url_for(".login_view")
            + '">Click here to log in.</a></p>'
        )
        self._template_args["form"] = form
        self._template_args["link"] = link
        return super(MyAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        logout_user()
        return redirect(url_for(".index"))

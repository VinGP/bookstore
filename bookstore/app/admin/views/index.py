from flask import redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_login import current_user, logout_user


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(".login_view", next=request.url))
        return super(MyAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        if current_user.is_authenticated:
            return redirect(url_for(".index"))
        return redirect(url_for("login", next=request.url))

    @expose("/register/", methods=("GET", "POST"))
    def register_view(self):
        if not current_user.is_authenticated:
            return redirect(url_for("register", next=request.url))
        return redirect(url_for(".index", next=request.url))

    @expose("/logout/")
    def logout_view(self):
        logout_user()
        return redirect(url_for(".index"))

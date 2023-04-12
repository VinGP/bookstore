from flask import abort, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_login import current_user, logout_user


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if current_user.is_authenticated and current_user.is_admin:
            return super(MyAdminIndexView, self).index()
        abort(404)

    @expose("/logout/")
    def logout_view(self):
        logout_user()
        return redirect(url_for("index"))

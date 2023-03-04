from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyBaseView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("login", next=request.url))

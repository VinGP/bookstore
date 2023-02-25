from config import Config
from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Authors, Books, Publishers, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

admin = Admin(app, name="microblog", template_mode="bootstrap3")


class BooksView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = True
    column_list = ("id", "author_id")
    form_columns = (
        "id",
        "title",
        "author_id",
    )


admin.add_view(BooksView(Books, db.session))
admin.add_view(ModelView(Publishers, db.session))
admin.add_view(ModelView(Authors, db.session))


@app.route("/")
def hello_world():
    return jsonify({"res": "Hello World!!!"})


@app.route("/i")
def i():
    return jsonify({"res": "i!!!"})


@app.route("/add/<n>")
def add(n):
    try:
        a = Authors(first_name="test", second_name="test")
        db.session.add(a)
        db.session.commit()
        at = {
            "first_name": a.first_name,
            "id": a.id,
            "second_name": a.second_name,
            "surname": a.surname,
        }

        p = Publishers("test")
        db.session.add(p)
        db.session.commit()
        pb = {"id": p.id, "name": p.name}
        b = Books("123423-1221-131-33", "test", 100, 2000, a.id, p.id)
        db.session.add(b)
        db.session.commit()
        bk = {"p": b.publisher_id, "a": a.id, "t": b.title}
        print(jsonify({"b": bk, "p": pb, "a": at}))
        return jsonify({"b": bk, "p": pb, "a": at})

    except Exception as e:
        return jsonify(e)


if __name__ == "__main__":
    app.run()

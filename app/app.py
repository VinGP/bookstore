from config import Config
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return jsonify({"res": "Hello World!!!"})


@app.route("/i")
def i():
    return jsonify({"res": "i!!!"})


@app.route("/add/<email>")
def add(email):
    try:
        u = User(email=email)
        db.session.add(u)
        db.session.commit()
        return jsonify({"email": u.email, "id": u.id, "active": u.active})
    except Exception as e:
        print(e)


@app.route("/get/<email>")
def get(email):
    users = User.query.all()
    # print(users)
    res = [{"email": u.email, "id": u.id, "active": u.active} for u in users]
    return jsonify({"res": res})


if __name__ == "__main__":
    app.run()

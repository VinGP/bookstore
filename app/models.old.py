from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(128))
    title = db.Column(db.Text())
    publication_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    available_quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publishers.id"), nullable=False)
    publisher = db.relationship("Publisher", back_populates="book")
    author = db.relationship("Author", back_populates="book")

    def __init__(
        self,
        isbn: str,
        title: str,
        available_quantity: int,
        price: int,
        author_id: int,
        publisher_id: int,
    ):
        self.isbn = isbn
        self.title = title
        self.available_quantity = available_quantity
        self.price = price
        self.author_id = author_id
        self.publisher_id = publisher_id


class Authors(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    second_name = db.Column(db.String(128), nullable=False)
    surname = db.Column(db.String(128))

    # books = db.relationship("Books", backref="authors")

    def __init__(self, first_name: str, second_name: str, surname: str = None):
        self.first_name = first_name
        self.second_name = second_name
        if surname is not None:
            self.surname = surname


class Publishers(db.Model):
    __tablename__ = "publishers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name: str):
        self.name = name

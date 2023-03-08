import os
import uuid

import sqlalchemy
from app import file_path
from flask_admin import form
from sqlalchemy import orm
from sqlalchemy.event import listens_for

from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = "books"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    isbn = sqlalchemy.Column(sqlalchemy.String(128))
    title = sqlalchemy.Column(sqlalchemy.String(255))
    publication_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.current_timestamp()
    )
    available_quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id"), nullable=False
    )
    author = orm.relationship("Author")
    publisher_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("publishers.id"), nullable=False
    )
    publisher = orm.relationship("Publisher")

    image = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)

    @staticmethod
    def generate_image_uuid():
        return str(uuid.uuid4())


@listens_for(Book, "after_delete")
def del_image(mapper, connection, target):
    if target.image:
        try:
            os.remove(os.path.join(file_path, target.image))

        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(os.path.join(file_path, form.thumbgen_filename(target.image)))
        except OSError:
            pass

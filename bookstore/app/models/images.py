import os
import uuid

import sqlalchemy
from app import file_path
from flask_admin import form
from sqlalchemy import orm
from sqlalchemy.event import listens_for

from .db_session import SqlAlchemyBase


class Image(SqlAlchemyBase):
    __tablename__ = "images"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    filename = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    book_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id"), nullable=False
    )
    book = orm.relationship("Book")

    @staticmethod
    def generate_image_uuid():
        return str(uuid.uuid4())


@listens_for(Image, "after_delete")
def del_image(mapper, connection, target):
    # if target.image:
    try:
        os.remove(os.path.join(file_path, target.filename))

    except OSError:
        pass

    # Delete thumbnail
    try:
        os.remove(os.path.join(file_path, form.thumbgen_filename(target.filename)))
    except OSError:
        pass


def generate_image_uuid():
    return str(uuid.uuid4())

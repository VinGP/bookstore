import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = "categories"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(400), index=True, unique=True)

    parent_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id")
    )
    parent = orm.relationship("Category", backref="children", remote_side=[id])

    def __repr__(self):
        if not self.parent:
            return self.name
        return str(self.parent) + "->" + self.name


books_categories = sqlalchemy.Table(
    "books_categories",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("books", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column(
        "categories", sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id")
    ),
)

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
    parent = orm.relationship(
        "Category", backref="children", remote_side=[id], post_update=True
    )

    def __repr__(self):
        if not self.parent or self.parent == self:
            return self.name
        return str(self.parent) + "->" + self.name

    @staticmethod
    def get_children_list(session, category_id):
        beginning_getter = (
            session.query(Category)
            .filter(Category.id == category_id)
            .cte(name="children_for", recursive=True)
        )
        with_recursive = beginning_getter.union_all(
            session.query(Category).filter(Category.parent_id == beginning_getter.c.id)
        )
        return session.query(with_recursive)

    @staticmethod
    def get_parents_list(session, category_id):
        beginning_getter = (
            session.query(Category)
            .filter(Category.id == category_id)
            .cte(name="parent_for", recursive=True)
        )
        with_recursive = beginning_getter.union_all(
            session.query(Category).filter(Category.id == beginning_getter.c.parent_id)
        )
        return session.query(with_recursive)


books_categories = sqlalchemy.Table(
    "books_categories",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("books", sqlalchemy.Integer, sqlalchemy.ForeignKey("books.id")),
    sqlalchemy.Column(
        "categories", sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id")
    ),
)

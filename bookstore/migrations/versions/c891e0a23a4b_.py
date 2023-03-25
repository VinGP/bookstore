"""empty message

Revision ID: c891e0a23a4b
Revises: 76e4c74608c4
Create Date: 2023-03-24 21:30:26.474023

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c891e0a23a4b"
down_revision = "76e4c74608c4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "carts_books", sa.Column("id", sa.Integer(), autoincrement=True, nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("carts_books", "id")
    # ### end Alembic commands ###

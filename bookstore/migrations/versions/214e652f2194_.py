"""empty message

Revision ID: 214e652f2194
Revises: 70ea6216ff1f
Create Date: 2023-03-22 13:32:41.853065

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "214e652f2194"
down_revision = "70ea6216ff1f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "series",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=True),
        sa.Column("publisher_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["publisher_id"],
            ["publishers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "books_series",
        sa.Column("books", sa.Integer(), nullable=True),
        sa.Column("series", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["books"],
            ["books.id"],
        ),
        sa.ForeignKeyConstraint(
            ["series"],
            ["series.id"],
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("books_series")
    op.drop_table("series")
    # ### end Alembic commands ###
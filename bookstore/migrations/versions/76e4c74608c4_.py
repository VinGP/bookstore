"""empty message

Revision ID: 76e4c74608c4
Revises: 214e652f2194
Create Date: 2023-03-23 13:28:26.038013

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "76e4c74608c4"
down_revision = "214e652f2194"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "books", ["isbn"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "books", type_="unique")
    # ### end Alembic commands ###
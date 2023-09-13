"""create posts table

Revision ID: d39d386dd657
Revises: 
Create Date: 2023-08-02 11:37:27.360335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd39d386dd657'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, nullable=False, primary_key=True), sa.Column("title", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table("posts")

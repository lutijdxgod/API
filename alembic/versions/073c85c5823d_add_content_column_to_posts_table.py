"""add content column to posts table

Revision ID: 073c85c5823d
Revises: d39d386dd657
Create Date: 2023-08-02 11:47:01.602600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '073c85c5823d'
down_revision = 'd39d386dd657'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")

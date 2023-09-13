"""add the other columns to posts table

Revision ID: 52ca3009ccf6
Revises: 151bbfc4392f
Create Date: 2023-08-02 22:26:41.023833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52ca3009ccf6'
down_revision = '151bbfc4392f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("published",
                    sa.Boolean, nullable=False,
                    server_default="FALSE")
                  )
    op.add_column("posts",
                  sa.Column("created_at",
                    sa.TIMESTAMP(timezone=True),
                    nullable=False,
                    server_default=sa.text("NOW()"))
                  )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
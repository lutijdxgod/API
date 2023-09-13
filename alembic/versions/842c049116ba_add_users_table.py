"""add users table

Revision ID: 842c049116ba
Revises: 073c85c5823d
Create Date: 2023-08-02 11:59:47.287439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '842c049116ba'
down_revision = '073c85c5823d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer, nullable=False),
                    sa.Column("email", sa.String, nullable=False),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )



def downgrade() -> None:
    op.drop_table("users")

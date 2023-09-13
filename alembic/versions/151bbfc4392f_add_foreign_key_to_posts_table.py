"""add foreign key to posts table

Revision ID: 151bbfc4392f
Revises: 842c049116ba
Create Date: 2023-08-02 22:19:49.490168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '151bbfc4392f'
down_revision = '842c049116ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fkey", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_user_fkey", table_name="posts")
    op.drop_column("posts", "owner_id")

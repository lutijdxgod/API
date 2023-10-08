"""added some logic for polls

Revision ID: 5b1ae9358560
Revises: 6b0b28b737b9
Create Date: 2023-10-06 00:16:40.093392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5b1ae9358560"
down_revision = "6b0b28b737b9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "polls",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("polls")
    # ### end Alembic commands ###

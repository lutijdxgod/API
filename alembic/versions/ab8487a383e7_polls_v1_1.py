"""polls v1.1

Revision ID: ab8487a383e7
Revises: 5b1ae9358560
Create Date: 2023-10-06 00:29:40.124591

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY


# revision identifiers, used by Alembic.
revision = "ab8487a383e7"
down_revision = "5b1ae9358560"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "poll_questions",
        sa.Column("entry_id", sa.Integer, nullable=False),
        sa.Column("poll_id", sa.Integer(), nullable=False),
        sa.Column("question", sa.String(), nullable=False),
        sa.Column(
            "answers", ARRAY(sa.String, dimensions=1, zero_indexes=True), nullable=False
        ),
        sa.ForeignKeyConstraint(["poll_id"], ["polls.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("entry_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("poll_questions")
    # ### end Alembic commands ###

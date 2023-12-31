"""added problem answers and comments to those answers

Revision ID: 4a526dd07529
Revises: 8fb0670ab31a
Create Date: 2023-10-13 01:20:16.467614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4a526dd07529"
down_revision = "8fb0670ab31a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "problem_answers",
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=True),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "images",
            postgresql.ARRAY(sa.String(), dimensions=1, zero_indexes=True),
            nullable=True,
            server_default="{}",
        ),
        sa.Column(
            "comments",
            postgresql.ARRAY(sa.Integer(), dimensions=1, zero_indexes=True),
            nullable=True,
            server_default="{}",
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"], ondelete="NO ACTION"),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("entry_id"),
    )
    op.create_table(
        "problem_answers_comments",
        sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("problem_answer_id", sa.Integer(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=True),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"], ondelete="NO ACTION"),
        sa.ForeignKeyConstraint(
            ["problem_answer_id"],
            ["problem_answers.entry_id"],
        ),
        sa.PrimaryKeyConstraint("entry_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("problem_answers_comments")
    op.drop_table("problem_answers")
    # ### end Alembic commands ###

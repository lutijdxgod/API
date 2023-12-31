"""added properties to user

Revision ID: 8d8f6265c971
Revises: 02068d2873bf
Create Date: 2023-10-15 01:22:15.933784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8d8f6265c971"
down_revision = "02068d2873bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("bio", sa.String(length=150), server_default="", nullable=False),
    )
    op.add_column(
        "users", sa.Column("rating", sa.Integer(), server_default="0", nullable=False)
    )
    op.add_column(
        "users",
        sa.Column("works_at_company", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "users",
        sa.Column(
            "amount_of_contacts", sa.Integer(), nullable=False, server_default="0"
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "amount_of_problem_answers",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "amount_of_problem_answers")
    op.drop_column("users", "amount_of_contacts")
    op.drop_column("users", "works_at_company")
    op.drop_column("users", "rating")
    op.drop_column("users", "bio")
    # ### end Alembic commands ###

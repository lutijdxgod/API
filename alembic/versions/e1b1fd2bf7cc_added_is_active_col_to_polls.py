"""added is_active col to polls

Revision ID: e1b1fd2bf7cc
Revises: 57c279d25d1a
Create Date: 2023-10-09 18:39:19.494978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1b1fd2bf7cc'
down_revision = '57c279d25d1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('polls', sa.Column('is_active', sa.Boolean(), server_default='True', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('polls', 'is_active')
    # ### end Alembic commands ###

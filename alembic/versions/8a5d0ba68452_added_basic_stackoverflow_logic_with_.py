"""added basic stackoverflow logic with tags

Revision ID: 8a5d0ba68452
Revises: fad115c5c847
Create Date: 2023-10-08 01:36:50.912638

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8a5d0ba68452'
down_revision = 'fad115c5c847'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('tag_id'),
    sa.UniqueConstraint('tag')
    )
    op.create_table('problems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('problem_tags',
    sa.Column('problem_id', sa.Integer(), nullable=False),
    sa.Column('tags', postgresql.ARRAY(sa.Integer(), dimensions=1, zero_indexes=True), server_default='{}', nullable=True),
    sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('problem_id')
    )
    op.add_column('poll_questions', sa.Column('entry_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('poll_questions', 'entry_id')
    op.drop_table('problem_tags')
    op.drop_table('problems')
    op.drop_table('tags')
    # ### end Alembic commands ###
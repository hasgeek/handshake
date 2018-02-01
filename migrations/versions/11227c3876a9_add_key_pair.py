"""add_key_pair

Revision ID: 11227c3876a9
Revises: 117e1c1968db
Create Date: 2018-02-01 21:18:38.848895

"""
from alembic import op
import sqlalchemy as sa


revision = '11227c3876a9'
down_revision = '117e1c1968db'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('keypair',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('puk', sa.Unicode(length=44), nullable=False),
        sa.Column('key', sa.Unicode(length=44), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key'),
        sa.UniqueConstraint('puk')
    )


def downgrade():
    op.drop_table('keypair')

"""init

Revision ID: 117e1c1968db
Revises: 
Create Date: 2018-02-01 14:40:59.353487

"""
from alembic import op
import sqlalchemy as sa
from coaster.sqlalchemy import JsonDict

revision = '117e1c1968db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('organization',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('userid', sa.Unicode(length=22), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(length=250), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('userid')
    )
    op.create_table('user',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False),
        sa.Column('userid', sa.String(length=22), nullable=False),
        sa.Column('lastuser_token_scope', sa.Unicode(length=250), nullable=True),
        sa.Column('lastuser_token_type', sa.Unicode(length=250), nullable=True),
        sa.Column('userinfo', JsonDict(), nullable=True),
        sa.Column('email', sa.Unicode(length=80), nullable=True),
        sa.Column('lastuser_token', sa.String(length=22), nullable=True),
        sa.Column('username', sa.Unicode(length=80), nullable=True),
        sa.Column('fullname', sa.Unicode(length=80), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('lastuser_token'),
        sa.UniqueConstraint('userid'),
        sa.UniqueConstraint('username')
    )
    op.create_table('workspace',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.Unicode(length=250), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('badge_template', sa.Unicode(length=2048), nullable=True),
        sa.Column('name', sa.Unicode(length=250), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('workspace_id', 'name'),
        sa.UniqueConstraint('workspace_id', 'title')
    )
    op.create_table('participant',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('fullname', sa.Unicode(length=80), nullable=False),
        sa.Column('email', sa.Unicode(length=254), nullable=False),
        sa.Column('verified_email', sa.Boolean(), nullable=True),
        sa.Column('phone', sa.Unicode(length=80), nullable=True),
        sa.Column('twitter', sa.Unicode(length=80), nullable=True),
        sa.Column('job_title', sa.Unicode(length=80), nullable=True),
        sa.Column('company', sa.Unicode(length=80), nullable=True),
        sa.Column('city', sa.Unicode(length=80), nullable=True),
        sa.Column('badge_printed', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('workspace_id', 'email')
    )
    op.create_table('ticket_client',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.Unicode(length=250), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('vendor_name', sa.Unicode(length=80), nullable=False),
        sa.Column('client_eventid', sa.Unicode(length=80), nullable=False),
        sa.Column('client_details', JsonDict(), server_default='{}', nullable=False),
        sa.Column('client_access_token', sa.Unicode(length=80), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_type',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(length=250), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('workspace_id', 'name')
    )
    op.create_table('contact_exchange',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('workspace_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspace.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'workspace_id', 'participant_id')
    )
    op.create_table('event_participant',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('checked_in', sa.Boolean(), nullable=False),
        sa.Column('checked_in_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
        sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id', 'participant_id')
    )
    op.create_table('event_ticket_type',
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.Column('ticket_type_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
        sa.ForeignKeyConstraint(['ticket_type_id'], ['ticket_type.id'], ),
        sa.PrimaryKeyConstraint('event_id', 'ticket_type_id')
    )
    op.create_table('ticket',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('ticket_no', sa.Unicode(length=80), nullable=False),
        sa.Column('order_no', sa.Unicode(length=80), nullable=False),
        sa.Column('ticket_type_id', sa.Integer(), nullable=False),
        sa.Column('participant_id', sa.Integer(), nullable=True),
        sa.Column('ticket_client_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['participant_id'], ['participant.id'], ),
        sa.ForeignKeyConstraint(['ticket_client_id'], ['ticket_client.id'], ),
        sa.ForeignKeyConstraint(['ticket_type_id'], ['ticket_type.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticket_client_id', 'order_no', 'ticket_no')
    )


def downgrade():
    op.drop_table('ticket')
    op.drop_table('event_ticket_type')
    op.drop_table('event_participant')
    op.drop_table('contact_exchange')
    op.drop_table('ticket_type')
    op.drop_table('ticket_client')
    op.drop_table('participant')
    op.drop_table('event')
    op.drop_table('workspace')
    op.drop_table('user')
    op.drop_table('organization')

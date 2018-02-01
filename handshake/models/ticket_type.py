# -*- coding: utf-8 -*-

from . import db
from .utils import ScopedNameTitleMixin


class TicketType(ScopedNameTitleMixin, db.Model):
    """Model different types of tickets."""

    __tablename__ = 'ticket_type'
    __table_args__ = (db.UniqueConstraint('workspace_id', 'name'),)

    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship('Workspace',
        backref=db.backref('ticket_types', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')
    events = db.relationship('Event', secondary='event_ticket_type')

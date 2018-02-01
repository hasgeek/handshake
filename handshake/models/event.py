# -*- coding: utf-8 -*-

from datetime import datetime
from . import db, BaseMixin
from .utils import ScopedNameTitleMixin

__all__ = ['Event']


event_ticket_type = db.Table('event_ticket_type', db.Model.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('ticket_type_id', db.Integer, db.ForeignKey('ticket_type.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)
)


class Event(ScopedNameTitleMixin, db.Model):
    """A discrete event under a workspace."""

    __tablename__ = 'event'
    __table_args__ = (db.UniqueConstraint('workspace_id', 'name'),
        db.UniqueConstraint('workspace_id', 'title'))

    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship('Workspace',
        backref=db.backref('events', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')
    ticket_types = db.relationship('TicketType', secondary=event_ticket_type)
    badge_template = db.Column(db.Unicode(2048), nullable=True)
    participants = db.relationship('Participant', secondary='event_participant', backref='events', lazy='dynamic')


class EventParticipant(BaseMixin, db.Model):
    """Join model between Participant and Event."""

    __tablename__ = 'event_participant'
    __table_args__ = (db.UniqueConstraint('event_id', 'participant_id'),)

    participant_id = db.Column(None, db.ForeignKey('participant.id'), nullable=False)
    participant = db.relationship('Participant',
        backref=db.backref('event_participants', cascade='all, delete-orphan'))
    event_id = db.Column(None, db.ForeignKey('event.id'), nullable=False)
    event = db.relationship(Event,
        backref=db.backref('event_participants', cascade='all, delete-orphan'))
    checked_in = db.Column(db.Boolean, default=False, nullable=False)
    checked_in_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @classmethod
    def get(cls, event, participant):
        return cls.query.filter_by(event=event, participant=participant).one_or_none()

# -*- coding: utf-8 -*-

import os
import base64
from datetime import datetime
from . import db, BaseMixin, Workspace, User, Event

__all__ = ['Participant']


def make_key():
    return base64.urlsafe_b64encode(os.urandom(128))


def make_public_key():
    return make_key()[:8]


def make_private_key():
    return make_key()[:8]


class Participant(BaseMixin, db.Model):
    """Model users participating in one or multiple events."""

    __tablename__ = 'participant'
    __table_args__ = (db.UniqueConstraint('workspace_id', 'email'),)

    fullname = db.Column(db.Unicode(80), nullable=False)
    #: Unvalidated email address
    email = db.Column(db.Unicode(254), nullable=False)
    #: Unvalidated phone number
    verified_email = db.Column(db.Boolean, default=False, nullable=True)
    phone = db.Column(db.Unicode(80), nullable=True)
    #: Unvalidated Twitter id
    twitter = db.Column(db.Unicode(80), nullable=True)
    #: Job title
    job_title = db.Column(db.Unicode(80), nullable=True)
    #: Company
    company = db.Column(db.Unicode(80), nullable=True)
    #: Participant's city
    city = db.Column(db.Unicode(80), nullable=True)
    badge_printed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship(User, backref=db.backref('participants', cascade='all, delete-orphan'))
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace,
        backref=db.backref('participants', cascade='all, delete-orphan'))

    @classmethod
    def get(cls, current_space, current_email):
        return cls.query.filter_by(workspace=current_space, email=current_email).one_or_none()

    @classmethod
    def upsert(cls, current_space, current_email, **fields):
        participant = cls.get(current_space, current_email)
        if participant:
            participant._set_fields(fields)
        else:
            participant = cls(workspace=current_space, email=current_email, **fields)
            db.session.add(participant)
        return participant

    def add_events(self, events):
        for event in events:
            if event not in self.events:
                self.events.append(event)

    def remove_events(self, events):
        for event in events:
            if event in self.events:
                self.events.remove(event)

    @classmethod
    def checkin_list(cls, event):
        """Return participant details along with their associated ticket types as a comma-separated string.
        WARNING: This query uses `string_agg` and hence will only work in PostgreSQL >= 9.0
        """
        participant_list = db.session.query('id', 'fullname', 'email', 'company', 'twitter', 'puk', 'key', 'checked_in', 'badge_printed', 'ticket_type_titles').from_statement(text('''
            SELECT distinct(participant.id), participant.fullname, participant.email, participant.company, participant.twitter,
                participant.puk, participant.key, attendee.checked_in, participant.badge_printed,
            (SELECT string_agg(title, ',') FROM sync_ticket
                INNER JOIN ticket_type ON sync_ticket.ticket_type_id = ticket_type.id
                WHERE sync_ticket.participant_id = participant.id) AS ticket_type_titles
            FROM participant INNER JOIN attendee ON participant.id = attendee.participant_id
            LEFT OUTER JOIN sync_ticket ON participant.id = sync_ticket.participant_id
            WHERE attendee.event_id = {event_id}
            ORDER BY participant.fullname
        '''.format(event_id=event.id))).all()
        return participant_list


class KeyPair(BaseMixin, db.Model):
    """A keypair for a participant inside a workspace."""

    __tablename__ = 'keypair'

    participant_id = db.Column(None, db.ForeignKey('participant.id'), nullable=False)
    participant = db.relationship('Participant',
        backref=db.backref('keypair', cascade='all, delete-orphan'))
    # public key
    # FIXME: Are two keys really required?
    puk = db.Column(db.Unicode(44), nullable=False, default=make_public_key, unique=True)
    key = db.Column(db.Unicode(44), nullable=False, default=make_private_key, unique=True)

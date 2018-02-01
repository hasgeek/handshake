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


class KeyPair(BaseMixin, db.Model):
    """A revocable keypair for a participant inside a workspace."""

    __tablename__ = 'keypair'

    participant_id = db.Column(None, db.ForeignKey('participant.id'), nullable=False)
    participant = db.relationship('Participant',
        backref=db.backref('keypair', cascade='all, delete-orphan'))
    # public key
    puk = db.Column(db.Unicode(44), nullable=False, default=make_public_key, unique=True)
    key = db.Column(db.Unicode(44), nullable=False, default=make_private_key, unique=True)

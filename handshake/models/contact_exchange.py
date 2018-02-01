# -*- coding: utf-8 -*-

from . import db, TimestampMixin

__all__ = ['ContactExchange']


class ContactExchange(TimestampMixin, db.Model):
    """Model to track who scanned whose badge"""

    __tablename__ = 'contact_exchange'

    user_id = db.Column(None, db.ForeignKey('user.id'), primary_key=True)
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), primary_key=True)
    participant_id = db.Column(None, db.ForeignKey('participant.id'), primary_key=True)

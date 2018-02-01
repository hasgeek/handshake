# -*- coding: utf-8 -*-

from . import Participant, Ticket, TicketType, BaseScopedNameMixin, Workspace, db, JsonDict

__all__ = ['TicketClient']


class TicketClient(BaseScopedNameMixin, db.Model):
    """Model an external ticketing service"""

    __tablename__ = 'ticket_client'

    name = db.Column(db.Unicode(80), nullable=False)
    vendor_name = db.Column(db.Unicode(80), nullable=False)
    client_eventid = db.Column(db.Unicode(80), nullable=False)
    client_details = db.Column(JsonDict, nullable=False, server_default='{}')
    client_access_token = db.Column(db.Unicode(80), nullable=False)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace,
        backref=db.backref('ticket_clients', cascade='all, delete-orphan'))

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

    def import_from_list(self, ticket_list):
        """
        Batch upserts the tickets and its associated ticket types and participants.
        Cancels the tickets in cancel_list.
        """

        for ticket_dict in ticket_list:
            ticket_type = TicketType.upsert(self.workspace, current_title=ticket_dict['ticket_type'])

            participant = Participant.upsert(self.workspace, ticket_dict['email'],
                fullname=ticket_dict['fullname'],
                phone=ticket_dict['phone'],
                twitter=ticket_dict['twitter'],
                company=ticket_dict['company'],
                job_title=ticket_dict['job_title'],
                city=ticket_dict['city']
            )

            ticket = Ticket.get(self, ticket_dict.get('order_no'), ticket_dict.get('ticket_no'))
            if ticket and (ticket.participant is not participant or ticket_dict.get('status') == u'cancelled'):
                # Ensure that the participant of a transferred or cancelled ticket does not have access to
                # this ticket's events
                ticket.participant.remove_events(ticket_type.events)

            if ticket_dict.get('status') == u'confirmed':
                ticket = Ticket.upsert(self, ticket_dict.get('order_no'), ticket_dict.get('ticket_no'),
                    participant=participant, ticket_type=ticket_type)
                # Ensure that the new or updated participant has access to events
                ticket.participant.add_events(ticket_type.events)

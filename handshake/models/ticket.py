# -*- coding: utf-8 -*-

from . import Participant, BaseMixin, db

__all__ = ['Ticket']


class Ticket(BaseMixin, db.Model):
    """Model for a ticket that was bought elsewhere. Eg: Boxoffice, Explara."""

    __tablename__ = 'ticket'
    __table_args__ = (db.UniqueConstraint('ticket_client_id', 'order_no', 'ticket_no'),)

    ticket_no = db.Column(db.Unicode(80), nullable=False)
    order_no = db.Column(db.Unicode(80), nullable=False)
    ticket_type_id = db.Column(None, db.ForeignKey('ticket_type.id'), nullable=False)
    ticket_type = db.relationship('TicketType',
        backref=db.backref('tickets', cascade='all, delete-orphan'))
    participant_id = db.Column(None, db.ForeignKey('participant.id'), nullable=True)
    participant = db.relationship('Participant', primaryjoin=participant_id == Participant.id,
        backref=db.backref('tickets', cascade="all, delete-orphan"))
    ticket_client_id = db.Column(db.Integer, db.ForeignKey('ticket_client.id'), nullable=False)
    ticket_client = db.relationship('TicketClient',
        backref=db.backref('tickets', cascade='all, delete-orphan'))

    @classmethod
    def get(cls, ticket_client, order_no, ticket_no):
        return cls.query.filter_by(ticket_client=ticket_client,
            order_no=order_no, ticket_no=ticket_no).one_or_none()

    @classmethod
    def upsert(cls, ticket_client, order_no, ticket_no, **fields):
        """
        Return a tuple containing the upserted ticket, and the participant the ticket,
        was previously associated with or None if there was no earlier participant.
        """
        ticket = cls.get(ticket_client, order_no, ticket_no)
        if ticket:
            ticket._set_fields(fields)
        else:
            fields.pop('ticket_client', None)
            fields.pop('order_no', None)
            fields.pop('ticket_no', None)
            ticket = cls(ticket_client=ticket_client, order_no=order_no, ticket_no=ticket_no, **fields)

            db.session.add(ticket)

        return ticket

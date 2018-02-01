# -*- coding: utf-8 -*-

from . import BaseScopedNameMixin, db, Organization

__all__ = ['Workspace']


class Workspace(BaseScopedNameMixin, db.Model):
    __tablename__ = 'workspace'

    organization_id = db.Column(None, db.ForeignKey('organization.id'), nullable=True)  # nullable for transition
    organization = db.relationship(Organization, backref=db.backref('spaces', cascade='all, delete-orphan'))
    parent = db.synonym('organization')

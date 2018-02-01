# -*- coding: utf-8 -*-

from . import db
from flask_lastuser.sqlalchemy import ProfileBase


class Organization(ProfileBase, db.Model):
    __tablename__ = 'organization'

    def permissions(self, user, inherited=None):
        perms = super(Organization, self).permissions(user, inherited)
        if self.userid in user.organizations_owned_ids():
            perms.add('org_admin')
        return perms

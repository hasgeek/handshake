# -*- coding: utf-8 -*-

from . import db
from flask_lastuser.sqlalchemy import ProfileBase


class Organization(ProfileBase, db.Model):
    __tablename__ = 'organization'

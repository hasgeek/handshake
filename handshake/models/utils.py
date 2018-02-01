# -*- coding: utf-8 -*-

from . import BaseScopedNameMixin

__all__ = ['ScopedNameTitleMixin']


class ScopedNameTitleMixin(BaseScopedNameMixin):
    # TODO: Move this into coaster?
    @classmethod
    def get(cls, parent, current_name=None, current_title=None):
        if not bool(current_name) ^ bool(current_title):
            raise TypeError("Expects current_name xor current_title")
        if current_name:
            return cls.query.filter_by(parent=parent, name=current_name).one_or_none()
        else:
            return cls.query.filter_by(parent=parent, title=current_title).one_or_none()

    @classmethod
    def upsert(cls, parent, current_name=None, current_title=None, **fields):
        instance = cls.get(parent, current_name, current_title)
        if instance:
            instance._set_fields(fields)
        else:
            fields.pop('title', None)
            instance = cls(parent=parent, title=current_title, **fields)
            db.session.add(instance)
        return instance

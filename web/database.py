# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
import logging

from flask import json
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext import mutable
from sqlalchemy.orm import relationship

from .compat import basestring
from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = relationship

logger = logging.getLogger('models')


def _get_or_create(cls, **kwargs):
    query = cls.query.filter_by(**kwargs)

    instance = query.first()

    if instance:
        return instance, False
    else:
        db.session.begin(nested=True)
        try:
            instance = cls(**kwargs)

            db.session.add(instance)
            db.session.commit()

            return instance, True
        except IntegrityError:
            db.session.rollback()
            instance = query.one()

            return instance, False


class JsonEncodedDict(db.TypeDecorator):
    impl = db.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

mutable.MutableDict.associate_with(JsonEncodedDict)


class Base(object):

    def __init__(self, **kwargs):
        super(Base, self).__init__()

    def to_dict(self):
        raise NotImplementedError

    @classmethod
    def factory(cls, **kwargs):
        instance, created = _get_or_create(cls, **kwargs)

        return instance


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""

        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.error(e)
                return False
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(Base, CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)

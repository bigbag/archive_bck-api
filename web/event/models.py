# -*- coding: utf-8 -*-

from web.database import Model, SurrogatePK, db


class Event(SurrogatePK, Model):

    __tablename__ = 'event'

    name = db.Column(db.String(150), nullable=False)
    key = db.Column(db.String(150), nullable=False)

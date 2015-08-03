# -*- coding: utf-8 -*-

from web.database import Model, SurrogatePK, db


class Term(SurrogatePK, Model):

    __tablename__ = 'term'

    id = db.Column(db.Integer, primary_key=True)
    hard_id = db.Column(db.Integer, unique=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(300), nullable=False)
    tz = db.Column(db.String(300), nullable=False)
    blacklist = db.Column(db.Integer)
    auth = db.Column(db.String(16))
    settings_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, index=True)

# -*- coding: utf-8 -*-
import logging

from web.database import Model, SurrogatePK, db

logger = logging.getLogger(__name__)


class Firm(SurrogatePK, Model):

    __tablename__ = 'firm'

    name = db.Column(db.String(300), nullable=False)

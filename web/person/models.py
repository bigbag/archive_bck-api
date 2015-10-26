# -*- coding: utf-8 -*-
import logging

from web.database import Model, SurrogatePK, db, ReferenceCol, relationship
from web.helpers import date_helper

logger = logging.getLogger(__name__)


class Person(SurrogatePK, Model):

    __tablename__ = 'person'

    PER_PAGE = 50

    STATUS_VALID = 1
    STATUS_BANNED = 0

    TYPE_TIMEOUT = 0
    TYPE_WALLET = 1

    SEARCH_KEY = ('name', 'tabel_id', 'card', 'hard_id')

    MANDATORY_PARAMETERS = ('name', 'tabel_id', 'hard_id')

    OPTIONAL_PARAMETERS = ('payment_id', 'card')

    name = db.Column(db.Text, nullable=False)
    tabel_id = db.Column(db.String(150))
    birthday = db.Column(db.Date())
    firm_id = ReferenceCol('firm', nullable=False)
    firm = relationship('Firm', backref='person')
    card = db.Column(db.String(8))
    payment_id = db.Column(db.String(20), nullable=False, index=True)
    hard_id = db.Column(db.String(128), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False, index=True)
    wallet_status = db.Column(db.Integer, nullable=False, index=True)
    type = db.Column(db.Integer, nullable=False, index=True)

    def __init__(self):
        self.status = self.STATUS_VALID
        self.wallet_status = self.STATUS_VALID
        self.type = self.TYPE_TIMEOUT
        self.creation_date = date_helper.get_current_date()
        self.name = u'Пользователь'

    @staticmethod
    def delete(person):
        try:
            db.session.query(PersonEvent).\
                filter(PersonEvent.person_id == person.id).delete()
            db.session.query(PersonWallet).\
                filter(PersonWallet.person_id == person.id).delete()
            db.session.delete(person)
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            logger.error(e)
            return False

        return True

    def to_dict(self):
        result = {
            'CardID': self.id,
            'Name': self.name,
            'TabelID': self.tabel_id,
            'Status': bool(self.status),
            'WalletStatus': bool(self.wallet_status),
        }
        person_wallet = {'Balance': 0}
        if len(self.corp_wallet) > 0:
            person_wallet = {'Balance': self.corp_wallet[0].balance}

        result.update(person_wallet)
        return result


class PersonEvent(SurrogatePK, Model):

    __tablename__ = 'person_event'

    STATUS_ACTIVE = 1
    STATUS_BANNED = 0

    person_id = ReferenceCol('person', nullable=False)
    person = relationship('Person', backref='person_event')
    term_id = ReferenceCol('term', nullable=False)
    term = relationship('Term', backref='person_event')
    event_id = ReferenceCol('event', nullable=False)
    event = relationship('Event', backref='person_event')
    firm_id = ReferenceCol('firm', nullable=False)
    firm = relationship('Firm', backref='person_event')
    timeout = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class PersonWallet(SurrogatePK, Model):

    __tablename__ = 'corp_wallet'

    person_id = ReferenceCol('person', nullable=False)
    person = relationship('Person', backref='corp_wallet')
    creation_date = db.Column(db.DateTime, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    limit = db.Column(db.Integer, nullable=False)
    interval = db.Column(db.Integer, nullable=False, index=True)
    status = db.Column(db.Integer, nullable=False, index=True)

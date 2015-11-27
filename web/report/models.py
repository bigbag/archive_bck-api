# -*- coding: utf-8 -*-

from web.database import Model, SurrogatePK, db, ReferenceCol, relationship

from web.helpers import date_helper


class Report(SurrogatePK, Model):

    __tablename__ = 'report'

    TYPE_WHITE = 0
    TYPE_PAYMENT = 1
    TYPE_MPS = 2

    CORP_TYPE_OFF = 0
    CORP_TYPE_ON = 1

    DEFAULT_PAGE = 1
    POST_ON_PAGE = 10

    STATUS_COMPLETE = 1
    STATUS_NEW = 0
    STATUS_FAIL = -1
    STATUS_LOST = -2

    id = db.Column(db.Integer, primary_key=True)
    term_id = ReferenceCol('term', nullable=False)
    term = relationship('Term', backref='report')
    event_id = db.Column(db.Integer)
    person_id = ReferenceCol('person', nullable=False)
    person = relationship('Person', backref='report')
    name = db.Column(db.Text, nullable=False)
    payment_id = db.Column(db.String(20))
    term_firm_id = db.Column(db.Integer, nullable=False)
    person_firm_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    corp_type = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        result = {
            'TranId': self.id,
            'CardID': 'N/A',
            'Date': date_helper.to_unixtime(self.creation_date),
            'Value': self.amount,
            'DeviceId': self.term.hard_id if self.term else 'N/A'
        }

        if self.person:
            result['CardID'] = self.person.card
        return result

    @staticmethod
    def get_by_current_date(interval, firms_id_list):
        query = Report.query.filter(Report.term_firm_id.in_(firms_id_list))
        query = query.filter(
            Report.creation_date.between(interval[0], interval[1]))

        return query.all()

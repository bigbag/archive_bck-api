# -*- coding: utf-8 -*-
import json
import logging

from flask import (abort, Blueprint, g, jsonify, request)

from web.person.models import Person, PersonWallet
from web.report.models import Report

from web.helpers import api_helper, date_helper, header_helper


logger = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix='/bck')


def get_parameters():

    try:
        search = json.loads(request.stream.read())
    except ValueError:
        return
    else:
        parameters = search.get('Parameter')
        if parameters:
            return parameters

    logger.debug('API: Not found Parameter in request parameters')
    return


def get_success_result(data=None):

    result = {
        'State': {
            'IsSuccess': True,
            'Code': '0000'
        }
    }
    try:
        len(data)
    except TypeError:
        pass
    else:
        result['Data'] = data
    return jsonify(result)


@blueprint.route("/GetCard/", methods=['POST'])
@header_helper.json_headers
def get_persons():

    limit = api_helper.get_request_count(
        request, Person.PER_PAGE, Person.MAX_PER_PAGE)

    offset = api_helper.get_request_offset(request)
    query = Person.query.filter(Person.firm_id.in_(g.firms))

    parameters = get_parameters()
    if parameters:
        cards_id = parameters.get('CardID')
        if cards_id:
            query = query.filter(Person.id.in_(cards_id))

    persons = query.limit(limit).offset(offset).all()

    if not persons:
        logger.debug('API: Not found persons')
        return get_success_result([])

    data = [person.to_dict() for person in persons]
    return get_success_result(data)


@blueprint.route("/UpdCard/", methods=['POST'])
@header_helper.json_headers
def create_or_update_person():

    parameters = get_parameters()
    if not parameters:
        abort(405)

    result = []
    for info in parameters:
        card_id = info.get('CardID')
        name = info.get('Name')
        tabel_id = info.get('TabelID')
        hard_id = info.get('HardID')
        payment_id = info.get('PaymentID')

        if not card_id or not name or not hard_id:
            logger.debug('API: Not valid parameters')
            continue

        query = Person.query.filter(Person.firm_id.in_(g.firms))

        person = query.filter_by(card=card_id).first()
        person_by_hard_id = query.filter_by(hard_id=hard_id).first()
        person_by_payment_id = query.filter_by(payment_id=payment_id).first()

        if person:
            if person_by_hard_id and person.id != person_by_hard_id.id:
                logger.debug('API: Not a unique value hard_id')
                continue

            if person_by_payment_id and person.id != person_by_payment_id.id:
                logger.debug('API: Not a unique value payment_id')
                continue
        else:
            person = Person()

        person.card_id = card_id
        person.name = name
        person.hard_id = hard_id
        person.firm_id = g.firms[0]

        if payment_id:
            person.payment_id = payment_id

        if tabel_id:
            person.tabel_id = tabel_id
        person.save()

        result.append(info)

    return get_success_result(result)


@blueprint.route("/DelCard/", methods=['POST'])
@header_helper.json_headers
def del_person():

    parameters = get_parameters()
    if not parameters:
        abort(405)

    card_id = parameters.get('CardID')
    if not card_id:
        logger.debug('API: Not found CardID in request parameters')
        abort(405)

    person = Person.query.filter(Person.firm_id.in_(g.firms)).\
        filter_by(id=card_id).first()
    if not person:
        logger.debug('API: Not found person')
        abort(404)

    result = Person.delete(person)
    if not result:
        abort(500)

    return get_success_result()


@blueprint.route("/UpdBalance/", methods=['POST'])
@header_helper.json_headers
def update_wallet_balance():

    parameters = get_parameters()
    if not parameters:
        abort(405)

    result = []
    for info in parameters:
        try:
            card = int(info.get('CardID'))
            balance = int(info.get('Balance'))
        except Exception as e:
            logger.debug('API: Not valid parameters')
            logger.debug(e)
            continue

        person = Person.query.filter_by(card=card)\
            .filter(Person.firm_id.in_(g.firms)).first()
        if not person:
            logger.debug('API: Not found persons with card %s' % card)
            continue

        person_wallet = PersonWallet.query.filter_by(person_id=person.id)\
            .first()
        if not person_wallet:
            logger.debug('API: Not found persons wallet for card %s' % card)
            continue

        person_wallet.balance = balance
        person_wallet.save()

        result.append(info)

    return get_success_result(result)


@blueprint.route("/GetTransactionLog/", methods=['POST'])
@header_helper.json_headers
def get_transaction_log():

    parameters = get_parameters()
    if not parameters:
        abort(405)

    try:
        date_begin = parameters.get('DateBegin')
        if date_begin:
            date_begin = int(date_begin)
        date_end = parameters.get('DateEnd')
        if date_end:
            date_end = int(date_end)
    except Exception as e:
        logger.debug('API: Not valid parameters')
        logger.debug(e)
        abort(405)

    if (date_begin and date_end) and (date_begin > date_end):
        abort(405)

    if not date_begin or not date_end:
        current_date = date_helper.get_current_utc()
        interval = date_helper.get_date_interval(current_date, 'month')
    else:
        interval = (
            date_helper.to_datetime(date_begin),
            date_helper.to_datetime(date_end)
        )

    reports = Report.get_by_current_date(interval, g.firms)
    result = [report.to_dict() for report in reports]

    return get_success_result(result)

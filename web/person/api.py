# -*- coding: utf-8 -*-
import json
import logging

from flask import (abort, Blueprint, g, jsonify, request, render_template)

from web.person.models import Person, PersonEvent

from web.helpers import api_helper, header_helper, logging_helper


logger = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix='/bck')


def get_parameter():
    try:
        search = json.loads(request.stream.read())
    except ValueError:
        return
    else:
        parameter = search.get('Parameter')
        if parameter:
            return parameter

    logger.debug('API: Not found Parameter in request parameters')
    return


@blueprint.route("/GetCard/", methods=['POST'])
@logging_helper.debug_request
@header_helper.json_headers
@api_helper.login_required
def get_persons():
    limit = api_helper.get_request_count(request, Person.PER_PAGE)
    offset = api_helper.get_request_offset(request)
    query = Person.query.filter(Person.firm_id.in_(g.firms))

    parameter = get_parameter()
    if parameter:
        cards_id = parameter.get('CardId')
        if cards_id:
            query = query.filter(Person.id.in_(cards_id))

    persons = query.limit(limit).offset(offset).all()
    if not persons:
        logger.debug('API: Not found persons')
        abort(404)

    data = [person.to_dict() for person in persons]

    result = {
        'Data': data,
        'State': {
            'IsSuccess': True,
            'Code': '0000'
        }
    }
    return jsonify(result)


@blueprint.route("/DelCard/", methods=['POST'])
@logging_helper.debug_request
@header_helper.json_headers
@api_helper.login_required
def del_person():

    parameter = get_parameter()
    if not parameter:
        abort(405)

    card_id = parameter.get('CardId')
    if not card_id:
        logger.debug('API: Not found CardId in request parameters')
        abort(405)

    person = Person.query.filter(Person.firm_id.in_(g.firms)).\
        filter_by(id=card_id).first()
    if not person:
        logger.debug('API: Not found person')
        abort(404)

    result = Person.delete(person)
    if not result:
        abort(500)

    result = {
        'State': {
            'IsSuccess': True,
            'Code': '0000'
        }
    }
    return jsonify(result)

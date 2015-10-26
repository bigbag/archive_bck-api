# -*- coding: utf-8 -*-
import json
import logging

from flask import (abort, Blueprint, g, jsonify, request, render_template)

from web.person.models import Person, PersonEvent

from web.helpers import api_helper, header_helper, logging_helper


logger = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix='/bck')


@blueprint.route("/GetCard/", methods=['POST'])
@logging_helper.debug_request
@header_helper.json_headers
@api_helper.login_required
def get_card():
    user = g.user

    limit = api_helper.get_request_count(request, Person.PER_PAGE)
    offset = api_helper.get_request_offset(request)
    query = Person.query.filter_by(firm_id=user.firm)

    try:
        search = json.loads(request.stream.read())
    except ValueError:
        pass
    else:
        parameter = search.get('Parameter')
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

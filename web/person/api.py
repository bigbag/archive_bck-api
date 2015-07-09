# -*- coding: utf-8 -*-
import logging

from flask import (abort, Blueprint, request, render_template)

from web.person.models import Person

from web.helpers import api_helper, header_helper, logging_helper


logger = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix='/terminal')


@blueprint.route("/firm_id/<int:firm_id>/persons/", methods=['GET'])
@logging_helper.debug_request
@header_helper.xml_headers
@api_helper.login_required
def getUsers(firm_id):

    search = {}
    for key in Person.SEARCH_KEY:
        search_value = request.args.get(key)
        if not search_value:
            continue
        search[key] = search_value

    limit = api_helper.get_request_count(request, Person.PER_PAGE)
    offset = api_helper.get_request_offset(request)
    query = Person.query.filter_by(firm_id=firm_id)
    if search:
        for key, value in search.iteritems():
            query = query.filter(getattr(Person, key).like('%' + value + '%'))

    persons = query.limit(limit).offset(offset).all()
    if not persons:
        logger.debug('API: Not found persons')
        abort(404)

    return render_template("person/person.xml", persons=persons)


@blueprint.route("/firm_id/<int:firm_id>/persons/", methods=['POST'])
@logging_helper.debug_request
@header_helper.xml_headers
@api_helper.login_required
def addUser(firm_id):
    search = {}
    for key in Person.MANDATORY_PARAMETERS:
        search_value = request.form.get(key)
        if not search_value:
            continue
        search[key] = search_value

    if len(search) != len(Person.MANDATORY_PARAMETERS):
        if not request.form.get(key):
            logger.debug('PERSON: Required parameters missing')
            abort(405)

    person = Person.query.filter_by(firm_id=firm_id).\
        filter((Person.hard_id == search['hard_id']) |
               (Person.tabel_id == search['tabel_id'])).first()

    if person:
        force = request.form.get('force')
        if not force:
            logger.debug('PERSON: Duplicate person')
            abort(400)

        result = Person.delete(person)
        if not result:
            abort(500)

    person = Person()
    person.firm_id = firm_id
    for key, value in search.iteritems():
        setattr(person, key, value)

    for key in Person.OPTIONAL_PARAMETERS:
        value = request.form.get(key)
        if not value:
            continue

        setattr(person, key, value)

    if not person.payment_id:
        person.payment_id = person.hard_id

    if not person.save():
        abort(500)

    return render_template("person/person.xml", persons=(person,))


@blueprint.route("/firm_id/<int:firm_id>/persons/", methods=['DELETE'])
@logging_helper.debug_request
@header_helper.xml_headers
@api_helper.login_required
def delUser(firm_id):
    hard_id = request.args.get('hard_id')
    if not hard_id:
        logger.debug('PERSON: Not found hard_id in request parameters')
        abort(405)

    person = Person.query.filter_by(firm_id=firm_id).\
        filter_by(hard_id=hard_id).first()
    if not person:
        logger.debug('PERSON: Not found person')
        abort(404)

    result = Person.delete(person)
    if not result:
        abort(500)

    return render_template("person/success.xml")

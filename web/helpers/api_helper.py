# -*- coding: utf-8 -*-
import logging
from flask import abort, g, current_app, request
from functools import wraps

from web.user.models import User

from web.helpers import hash_helper

logger = logging.getLogger(__name__)


def access_check():
    headers = request.headers
    if 'Key' not in headers or 'Sign' not in headers:
        logger.debug('API: Not found "Key" or "Sign" in request headers')
        return False

    user = User.query.filter_by(key=headers['Key']).first()
    if not user:
        logger.debug('API: Not found user')
        return False

    g.firms = (user.firm).split(',')

    app = (x for x in user.app.split(','))
    if current_app.config.get('API_PROJECT_NAME') not in app:
        logger.debug('API: No access to the selected app')
        return False

    true_sign = hash_helper.get_api_sign(
        str(user.secret),
        dict(request.form.items() + request.args.items()))

    if not true_sign == headers['Sign']:
        logger.debug('API: No valid "Sign"')
        logger.debug('API: True "Sign" is %s' % true_sign)
        return False

    return True


def get_request_count(request, default, max=None):
    limit = request.args.get('count', default)
    try:
        limit = int(limit)
    except:
        abort(405)
    if max and limit > max:
        limit = max

    return limit


def get_request_offset(request):
    offset = request.args.get('offset', 0)
    try:
        offset = int(offset)
    except:
        abort(405)

    return offset

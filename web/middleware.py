# -*- coding: utf-8 -*-

from flask import abort

from web.helpers import api_helper, logging_helper


class AppMiddleware(object):

    def __init__(self, app):
        self.init_app(app)

    def init_app(self, app):

        @app.before_request
        def init_middleware():
            if app.config.get('DEBUG_HTTP_REQUEST'):
                logging_helper.debug_http_request()

            if app.config.get('API_REQUIRED_PASSWORD'):
                if not api_helper.access_check():
                    abort(403)

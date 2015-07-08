# -*- coding: utf-8 -*-
import logging

from flask import Flask, render_template

from web import person
from web.extensions import bcrypt, db
from web.helpers.header_helper import xml_headers

try:
    from web.settings_local import Config
except Exception as e:
    logging.exception("Exception: %(body)s", {'body': e})
    from web.settings import Config


def create_app(config_object=Config):

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):

    bcrypt.init_app(app)
    db.init_app(app)
    return None


def register_blueprints(app):
    app.register_blueprint(person.api.blueprint)

    return None


def register_errorhandlers(app):
    @xml_headers
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("errors/{0}.xml".format(error_code)), error_code
    for errcode in [401, 403, 404, 405, 500]:
        app.errorhandler(errcode)(render_error)
    return None

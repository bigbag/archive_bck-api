#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask.ext.script import Manager, Server, Shell

from web.app import create_app
from web.database import db

from web.event.models import Event
from web.firm.models import Firm
from web.person.models import Person, PersonEvent
from web.user.models import User

try:
    from web.settings_local import Config
except Exception as e:
    logging.exception("Exception: %(body)s", {'body': e})
    from web.settings import Config

app = create_app(Config)
manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app,
            'db': db,
            'User': User,
            'Firm': Firm,
            'Person': Person,
            'PersonEvent': PersonEvent,
            'Event': Event}


manager.add_command('server', Server(host=app.config['APP_HOST'],
                                     port=app.config['APP_PORT']))
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()

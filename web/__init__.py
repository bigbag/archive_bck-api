# -*- coding: utf-8 -*-
import logging
from web.app import create_app

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

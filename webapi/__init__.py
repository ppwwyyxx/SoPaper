# -*- coding: utf-8 -*-
# $File: __init__.py
# $Date: Mon Mar 24 12:03:16 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""uknow informatin hub API website"""

import os
from flask import Flask

from flask_login import LoginManager

from ukutil import import_all_modules


class DefaultConfig(object):
    API_HOST = '0.0.0.0'
    API_PORT = None
    API_RUN_OPTIONS = {}

_app = None
login_manager = None


def get_app():
    """load API modules and return the WSGI application"""
    global get_app, _app, login_manager
    _app = Flask(__name__,
                 instance_relative_config=True,
                 instance_path=os.environ.get('SOA_CONFIG'))
    _app.config.from_object(DefaultConfig())

    _app.secret_key = 'WTF is this!!'       # Should have this to work

    login_manager = LoginManager()
    login_manager.init_app(_app)

    import_all_modules(__file__, __name__)
    get_app = lambda: _app
    return _app

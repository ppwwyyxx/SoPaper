#!./manage/exec-in-virtualenv.sh
# -*- coding: utf-8 -*-
# $File: standalone_server.py
# $Author: jiakai <jia.kai66@gmail.com>

from webapi import get_app
import signal
import sys
import os
import os.path


def sigint_handler(s, f):
    """receive the SIGINT signal from unittest script
    and exit correctly"""
    print('api standalone server: SIGINT received, exit')
    sys.exit()


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    app = get_app()
    try:
        app.config.from_pyfile('../manage/api_website_config.py')
    except IOError as e:
        print(e)
        print('WARNING: No configuration found, using builtin defaults.')

    app.run(app.config['API_HOST'], app.config['API_PORT'],
            **app.config['API_RUN_OPTIONS'])

if __name__ == "__main__":
    main()

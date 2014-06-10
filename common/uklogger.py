#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: uklogger.py
# $Date: 一 6月 09 17:20:34 2014 +0000
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for handling logging"""

import ukconfig
import traceback
import time
import os
import os.path
from termcolor import colored


def log_api(msg):
    """log a message from api-website"""
    print colored('API', 'green'), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_info(msg):
    """log an info message"""
    print colored('INFO', 'blue'), msg
    if ukconfig.LOG_DIR:
        with open(os.path.join(ukconfig.LOG_DIR, 'info.txt'), 'a') as f:
            f.write(msg)
            f.write('\n')
    # TODO: use log util, log to file, including time, module, etc.


def log_err(msg):
    """log an err message"""
    print colored('ERR', 'red', attrs=['blink']), msg
    if ukconfig.LOG_DIR:
        with open(os.path.join(ukconfig.LOG_DIR, 'error.txt'), 'a') as f:
            f.write(msg)
            f.write('\n')
    # TODO: use log util, log to file, including time, module, etc.

def log_exc(exc):
    """log an unexpected exception"""
    log_err('Caught unexpected exception: {}\n{}'.format(
        exc, traceback.format_exc()))

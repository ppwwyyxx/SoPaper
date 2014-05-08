#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: uklogger.py
# $Date: Fri Apr 18 23:32:56 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""utilities for handling logging"""

import traceback
import time
from termcolor import colored


def log_api(msg):
    """log a message from api-website"""
    print colored('API', 'green'), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_info(msg):
    """log an info message"""
    print colored('INFO', 'blue'), msg
    # TODO: use log util, log to file, including time, module, etc.


def log_err(msg):
    """log an err message"""
    print colored('ERR', 'red', attrs=['blink']), msg
    # TODO: use log util, log to file, including time, module, etc.

def log_query(msg):
    """log all the queries"""
    print colored('QUERY', 'green', attrs=['blink']), msg
    try:
        with open('/home/soa/query-log.txt', 'a') as f:
            print >> f, time.ctime(), msg
    except:
        pass

def log_exc(exc):
    """log an unexpected exception"""
    log_err('Caught unexpected exception: {}\n{}'.format(
        exc, traceback.format_exc()))

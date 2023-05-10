#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: mark.py
# Author: Yichen Wang <wangycthu@gmail.com>

from uklogger import *
from . import api_method, request
from ukdbconn import get_mongo

# api: /getmark?pid=2
@api_method('/getmark')
def mark():
    """ get marks of the paper with pid """
    try:
        pid = int(request.values.get('pid'))
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    db = get_mongo('paper')
    res = db.find_one({'_id': pid}, {'upvote': 1, 'downvote': 1})
    log_info("Return marks of pdf {0}".format(pid))

    if res is None:
        return {}
    return res

# api: /mark?pid=2&mark=1,-1
# 1: good  -1: bad
@api_method('/mark')
def do_mark():
    """ update db with user's mark & uid """
    try:
        pid = int(request.values.get('pid'))
        mark = int(request.values.get('mark'))
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    db = get_mongo('paper')
    if mark == 1:
        db.update({'_id': pid}, {'$inc': {'upvote': 1}})
    else:
        db.update({'_id': pid}, {'$inc': {'downvote': 1}})
    log_info("Add mark to pdf {0}".format(pid))

    return {'status': 'ok'}

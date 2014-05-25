#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: getcmt.py
# Author: Yichen Wang <wangycthu@gmail.com>

from uklogger import *
from . import api_method, request
from ukdbconn import get_mongo

# api: /getcmt?pid=2&page=0,1,2...
@api_method('/getcmt')
def get_comment():
    """ return first 10 comments of the paper with pid """
    try:
        pid = long(request.values.get('pid'))
        page = int(request.values.get('page'))
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    db = get_mongo('paper')
    res = db.find_one({'_id': pid}, {'comments': {'$slice': [page*10, 10]}, 'cmt_count': 1})
    log_info("Return 10 comments of paper {0}".format(pid))

    if res is None:
        return {}
    return res

# api: /getmark?pid=2
@api_method('/getmark')
def do_mark():
    """ get marks of the paper with pid """
    try:
        pid = long(request.values.get('pid'))
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    db = get_mongo('paper')
    res = db.find_one({'_id': pid}, {'upvote': 1, 'downvote': 1})
    log_info("Return marks of pdf {0}".format(pid))

    if res is None:
        return {}
    return res

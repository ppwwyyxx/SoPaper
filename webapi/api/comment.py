#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: comment.py
# Author: Yichen Wang <wangycthu@gmail.com>

from uklogger import *
from . import api_method, request
from ukdbconn import get_mongo

# api: /comment?pid=2&uid=xxx&cmt=xxxx
@api_method('/comment')
def do_comment():
    """ update db with user's comment & uid """
    try:
        pid = int(request.values.get('pid'))
        uid = request.values.get('uid')
        comment = request.values.get('cmt')
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    db = get_mongo('paper')
    db.update({'_id': pid}, {'$push': {'comments': {'cmt': comment, 'uid': uid}}})
    db.update({'_id': pid}, {'$inc': {'cmt_count': 1}})
    log_info("Add {0}'s comment to pdf {1}".format(uid, pid))

    return {'status': 'ok'}

# api: /getcmt?pid=2&page=0,1,2...
@api_method('/getcmt')
def get_comment():
    """ return first 10 comments of the paper with pid """
    try:
        pid = int(request.values.get('pid'))
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


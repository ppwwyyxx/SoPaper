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
        pid = long(request.values.get('pid'))
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

# api: /mark?pid=2&mark=1,-1
# 1: good  -1: bad
@api_method('/mark')
def do_mark():
    """ update db with user's mark & uid """
    try:
        pid = long(request.values.get('pid'))
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

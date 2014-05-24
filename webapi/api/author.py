#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: author.py
# Author: Yichen Wang <wangycthu@gmail.com>

from uklogger import *
from . import api_method, request
from ukdbconn import get_mongo
from dbsearch import SEARCH_RETURN_FIELDS

# api: /author?name=xxx
@api_method('/author')
def search_author():
    """ search db by author name
        return a list of paper info """
    try:
        name = request.values.get('name')
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    db = get_mongo('paper')
    res = list(db.find({'author': name}, SEARCH_RETURN_FIELDS))

    return {'status': 'ok',
            'res': res}

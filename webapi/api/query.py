#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: query.py
# Date: Fri May 23 21:26:10 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from lib.textutil import title_beautify
from queryhandler import handle_title_query, handle_content_query

# api: /query?q=test
@api_method('/query')
def query():
    """ first try title-search, then content-search """
    query = request.values.get('q')

    tp = 'title'
    res = handle_title_query(query)
    if not res:
        res = handle_content_query(query)
        tp = 'content'

    return {'status': 'ok',
            'type': tp,
            'results': res}

# api: /cquery?q=test
@api_method('/cquery')
def content_query():
    """ only use content-search backend """
    query = request.values.get('q')
    res = handle_content_query(query)
    return {'status': 'ok',
            'type': 'content',
            'results': res
           }


#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: query.py
# Date: Sun May 25 22:50:40 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from lib.textutil import title_beautify
from queryhandler import handle_title_query, handle_content_query


def transform(r):
    if r.get('page'):
        r['haspdf'] = 1
    else:
        r['haspdf'] = 0

    try:
        r['citecnt'] = len(r['citedby'])
        del r['citedby']
    except:
        r['citecnt'] = 0
    return r

def do_query(query):
    tp = 'title'
    res = handle_title_query(query)
    if not res:
        res = handle_content_query(query)
        tp = 'content'

    assert isinstance(res, list)

    res = map(transform, res)
    return {'status': 'ok',
            'type': tp,
            'results': res}

# api: /query?q=test
@api_method('/query')
def query():
    """ first try title-search, then content-search """
    query = request.values.get('q')
    return do_query(query)


# api: /cquery?q=test
@api_method('/cquery')
def content_query():
    """ only use content-search backend """
    query = request.values.get('q')
    res = handle_content_query(query)
    assert isinstance(res, list)

    res = map(transform, res)

    return {'status': 'ok',
            'type': 'content',
            'results': res
           }


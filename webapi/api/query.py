#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: query.py
# Date: 六 6月 14 03:17:06 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import math
from . import api_method, request
from lib.textutil import title_beautify
from queryhandler import handle_title_query, handle_content_query, handl_author_query
from ukdbconn import get_mongo
from dbsearch import SEARCH_RETURN_FIELDS


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
    if 'author' in r:
        r['author'] = [title_beautify(x) for x in r['author']]
    r['title'] = title_beautify(r['title'])
    return r

def sort_content(res):
    def score(r):
        w = r['weight']
        c = r['citecnt']
        c = max([c, 10])
        return (w ** 2) * c

    print([r['weight']  for r in res])
    print([r['citecnt'] for r in res])
    print([score(r) for r in res])
    res = sorted(res, key=score)
    return res

def do_query(query):
    tp = 'title'
    res = handle_title_query(query)
    if not res:
        res = do_search_author(query)
        if res:
            return res
        res = handle_content_query(query)
        tp = 'content'

    assert isinstance(res, list)

    res = list(map(transform, res))

    if tp == 'content':
        res = sort_content(res)
    return {'status': 'ok',
            'type': tp,
            'results': res}

# api: /query?q=test
@api_method('/query')
def query():
    """ first try title-search, then content-search """
    query = request.values.get('q')
    if query == 'None':
        return {'status': 'error',
                'reason': 'invalid request'}
    return do_query(query)


# api: /cquery?q=test
@api_method('/cquery')
def content_query():
    """ only use content-search backend """
    try:
        query = request.values.get('q')
        assert query != "None"
    except:
        return {'status': 'error',
                'reason': 'invalid request'}

    res = handle_content_query(query)
    assert isinstance(res, list)
    res = list(map(transform, res))

    return {'status': 'ok',
            'type': 'author',
            'results': res}
    res = sort_content(res)

    return {'status': 'ok',
            'type': 'content',
            'results': res
           }

def do_search_author(name):
    res = handl_author_query(name)
    if not res:
        return None

    res = list(map(transform, res))
    res = sorted(res, key=lambda x: x.get('citecnt', 0))
    return {'status': 'ok',
            'type': 'author',
            'results': res}


# api: /author?name=xxx
@api_method('/author')
def search_author():
    """ search db by author name
        return a list of paper info """
    try:
        name = request.values.get('name').lower()
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}

    ret = do_search_author(name)
    if ret:
        return ret
    else:
        return {'status': 'ok',
                'type': 'author',
                'results': []}

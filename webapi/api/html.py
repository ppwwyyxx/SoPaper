#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: html.py
# Date: Tue May 20 18:01:39 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from ukdbconn import get_mongo

# api: /html?pid=2&page=0,1,3,5
# 0 is the html framework
@api_method('/html')
def html():
    """ return a dict of {pagenum: 'html'} """
    try:
        pid = int(request.values.get('pid'))
        page_str = request.values.get('page')
        pages = list(map(int, page_str.split(',')))
    except Exception:
        return {'status': 'error',
                'reason': 'invalid request'}
    db = get_mongo('paper')
    doc = db.find_one({'_id': pid}, {'page': 1, 'html': 1})

    if max(pages) > doc['page'] or min(pages) < 0:
        return {'status': 'error',
                'reason': 'invalid page index'}

    res = {}
    for p in pages:
        res[p] = doc['html'][p]
    return {'status': 'ok',
            'htmls': res }

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: query.py
# Date: Sun May 11 13:19:35 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from lib.textutil import title_beautify
from search import handle_query

# api: /query?q=test
@api_method('/query')
def query():
    """ give a query, return paperid
        TODO: return list of paperid if no good candidates found
    """
    query = request.values.get('q')

    res = handle_query(query)
    return {'status': 'ok',
            'results': res}


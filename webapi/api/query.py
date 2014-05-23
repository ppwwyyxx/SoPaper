#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: query.py
# Date: Fri May 23 20:26:45 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request
from lib.textutil import title_beautify
from queryhandler import handle_title_query

# api: /query?q=test
@api_method('/query')
def query():
    """ give a query, return paperid
        TODO: return list of paperid if no good candidates found
    """
    query = request.values.get('q')

    res = handle_title_query(query)
    return {'status': 'ok',
            'results': res}


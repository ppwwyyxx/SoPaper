#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: query.py
# Date: Sat May 10 20:23:15 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import api_method, request

# api: /query?q=test
@api_method('/query')
def query():
    """ give a query, return paperid
        TODO: return list of paperid if no good candidates found
    """
    query = request.values.get('q')

    return {'pid': 1}


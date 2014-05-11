#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dbsearch.py
# Date: Sun May 11 13:43:39 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from ukdbconn import get_mongo
from uklogger import *
from lib.textutil import title_beautify

def beautify_results():
    def wrap(func):
        def call(query):
            res = func(query.lower())
            for k in res:
                k['title'] = title_beautify(k['title'])
            return res
        return call
    return wrap

@beautify_results()
def search_exact(query):
    db = get_mongo('paper')
    res = list(db.find({'title': query},
                       {'view_cnt': 1, 'download_cnt': 1, 'title': 1}
                      ))
    return res

@beautify_results()
def search_startswith(query):
    db = get_mongo('paper')
    res = list(db.find({'title': {'$regex': '^{0}'.format(query) } },
                       {'view_cnt': 1, 'download_cnt': 1, 'title': 1}
                      ))
    return res

@beautify_results()
def search_regex(regex):
    db = get_mongo('paper')
    res = list(db.find({'title': {'$regex':
                                  '{0}'.format(query) }
                       }, {'view_cnt': 1, 'download_cnt': 1, 'title': 1}
                      ))
    return res

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: search.py
# Date: Sun May 11 13:29:55 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from ukdbconn import get_mongo
from uklogger import *
from lib.textutil import title_beautify
import searcher
import fetcher
from job import JobContext

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


def handle_query(query):
    query = title_beautify(query)
    log_info("Get query: {0}".format(query))
    res = search_startswith(query)
    if res:
        log_info("Found {0} results in db".format(len(res)))
        return res
    searchers = searcher.register_searcher.get_searcher_list()
    parsers = fetcher.register_parser.get_parser_list()
    ctx = JobContext(query)

    return

    for s in searchers:
        srs = s.run(ctx)

        # try search database with updated title
        if ctx.title != query:
            query = ctx.title
            res = search_exact(query)
            if res:
                log_info("Found {0} results in db".format(len(res)))
                return res

        for sr in srs:
            for parser in parsers:
                succ = parser.run(ctx, sr)
                if not succ:
                    continue
                if ctx.existing is not None:
                    log_info("Found {0} results in db".format(len(ctx.existing)))
                    return ctx.existing
                try:
                    pid = ukdbconn.new_paper(ctx)
                    return {'_id': pid,
                            'title': ctx.title,
                            'view_cnt': 1,
                            'download_cnt': 0
                           }
                except:
                    log_exc("Failed to save to db")

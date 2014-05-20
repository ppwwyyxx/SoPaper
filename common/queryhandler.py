#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: queryhandler.py
# Date: Tue May 20 14:26:12 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import ukdbconn
from uklogger import *
from lib.textutil import title_beautify
import searcher
import fetcher
from job import JobContext
from dbsearch import *

def handle_query(query):
    query = title_beautify(query)
    log_info("Get query: {0}".format(query))
    # starts search
    res = search_startswith(query)
    if res:
        log_info("Found {0} results in db".format(len(res)))
        return res
    # similar search
    res = similar_search(query)
    if res:
        log_info("Found similar results in db: {0}".format(res['title']))
        return [res]

    # search on web
    searchers = searcher.register_searcher.get_searcher_list()
    parsers = fetcher.register_parser.get_parser_list()
    ctx = JobContext(query)

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
                    return [{'_id': pid,
                            'title': ctx.title,
                            'view_cnt': 1,
                            'download_cnt': 0
                           }]
                except:
                    log_exc("Failed to save to db")

if __name__ == '__main__':
    res = handle_query('test file')
    print res


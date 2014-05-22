#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: queryhandler.py
# Date: Thu May 22 11:01:54 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from bson.binary import Binary
from threading import Thread

from ukdbconn import get_mongo, global_counter
from uklogger import *
from lib.textutil import title_beautify, parse_file_size
import searcher
import fetcher
from job import JobContext
from dbsearch import *
from pdfprocess import pdf_postprocess

def new_paper(ctx):
    pid = global_counter('paper')
    log_info("Add new paper: {0}, size={1}, pid={2}".format(
        ctx.title, parse_file_size(len(ctx.data)), pid))
    doc = {
        '_id': pid,
        'pdf': Binary(ctx.data),
        'title': ctx.title.lower(),
        'view_cnt': 1,
        'download_cnt': 0
    }
    doc.update(ctx.meta)

    db = get_mongo('paper')
    db.ensure_index('title')
    ret = db.insert(doc)

    thread = Thread(target=pdf_postprocess, args=(ctx.data, pid))
    thread.start()
    return pid


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
                    pid = new_paper(ctx)
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


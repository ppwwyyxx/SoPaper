#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: queryhandler.py
# Date: Sat May 24 00:03:37 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from bson.binary import Binary
from threading import Thread
from multiprocessing import Pool

from ukdbconn import get_mongo, global_counter
from uklogger import *
from lib.textutil import title_beautify, parse_file_size
import searcher
import fetcher
from job import JobContext
from dbsearch import *
from pdfprocess import pdf_postprocess

from contentsearch import SoPaperSearcher

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

    thread = Thread(target=pdf_postprocess, args=(ctx, pid))
    thread.start()
    return pid

def search_run(searcher, ctx):
    return searcher.run(ctx)

def handle_title_query(query):
    query = title_beautify(query)
    log_info("Get title query: {0}".format(query))
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

    args = zip(searchers, [ctx] * len(searchers))
    pool = Pool()
    as_results = [pool.apply_async(search_run, arg) for arg in args]

    for s in as_results:
        s = s.get()
        srs = s['results']

        # try search database with updated title
        try:
            updated_title = s['ctx_update']['title']
        except KeyError:
            pass
        else:
            if updated_title != query:
                query = updated_title
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
                    ret = [{'_id': pid,
                            'title': ctx.title,
                            'view_cnt': 1,
                            'download_cnt': 0
                           }]
                    ret[0].update(ctx.meta)
                except:
                    log_exc("Failed to save to db")

sp_searcher = SoPaperSearcher()
def handle_content_query(query):
    log_info("Get content query: {0}".format(query))
    res = sp_searcher.search(query)
    return res

if __name__ == '__main__':
    #res = handle_title_query('test test test this is not a paper name')
    res = handle_content_query('from')
    print res


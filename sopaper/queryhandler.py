#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: queryhandler.py
# Date: Thu Jun 18 22:52:39 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from bson.binary import Binary
from threading import Thread
from multiprocessing import Pool

from ukdbconn import get_mongo, global_counter, new_paper
from uklogger import *
from lib.textutil import title_beautify, parse_file_size
import searcher
from searcher import searcher_run
import fetcher
from job import JobContext
from dbsearch import *
from pdfprocess import postprocess
from lib.downloader import ProgressPrinter
from contentsearch import SoPaperSearcher
import ukconfig

# global. save all ongoing download
progress_dict = {}

class Updater(ProgressPrinter):
    def __init__(self, pid):
        self.pid = pid
        super(Updater, self).__init__()

    def update(self, done):
        percent = float(done) / self.total
        progress_dict[self.pid] = percent
        super(Updater, self).update(done)

def start_download(dl_candidates, ctx, pid):
    dl_candidates = sorted(dl_candidates, key=lambda x: x[0].priority,
                           reverse=True)
    updater = Updater(pid)
    for (parser, sr) in dl_candidates:
        data = parser.download(sr, updater)
        if data:
            db = get_mongo('paper')
            try:
                db.update({'_id': pid},
                          {'$set': {
                            'pdf': Binary(data),
                            'page_url': sr.url,
                            'source': parser.name
                          }})
            except:
                log_exc("Save pdf data error")
            postprocess(data, ctx, pid)
            progress_dict.pop(pid, None)
            return
    progress_dict.pop(pid, None)

def handle_title_query(query):
    query = title_beautify(query)
    log_info("Get title query: {0}".format(query))

     #starts search
    res = search_startswith(query) # and the idf is large
    if res:
        log_info("Found {0} results in db: {1}".format(
            len(res), str([x['_id'] for x in res])))
        return res
    # similar search
    res = similar_search(query)
    if res:
        log_info(u"Found similar results in db: {0}".format(res['_id']))
        return [res]

    # search on web
    searchers = searcher.register_searcher.get_searcher_list()
    parsers = fetcher.register_parser.get_parser_list()
    ctx = JobContext(query)

    args = zip(searchers, [ctx] * len(searchers))
    pool = Pool()
    async_results = [pool.apply_async(searcher_run, arg) for arg in args]

    # Search and get all the results item
    all_search_results = []
    for s in async_results:
        s = s.get(ukconfig.PYTHON_POOL_TIMEOUT)
        if s is None:
            continue
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
                    log_info("Found {0} results in db: {1}".format(
                        len(res), str([x['_id'] for x in res])))
                    return res
        all_search_results.extend(srs)

        meta = s.get('ctx_update')
        if meta:
            log_info('Meat update from searcher: {0}'.format(str(meta.keys())))
            ctx.update_meta_dict(meta)
    pool.close()
    pool.terminate()

    # Analyse each result and try to parse info
    download_candidates = []
    parser_used = set()
    found = False
    for sr in all_search_results:
        for parser in parsers:
            if parser.can_handle(sr):
                download_candidates.append((parser, sr))
                if ctx.need_field(parser.support_meta_field):
                    # Already tried this fetcher
                    if not parser.repeatable and \
                            parser.name in parser_used:
                        continue
                    else:
                        parser_used.add(parser.name)

                    succ = parser.fetch_info(ctx, sr)
                    if not succ:
                        continue
                    found = True
                    if ctx.existing is not None:
                        log_info("Found {0} results in db".format(len(ctx.existing)))
                        return [ctx.existing]

    # no metadata or downloadable source found
    if not found and len(download_candidates) == 0:
        return None
    # Save data, return data and start downloading
    try:
        pid = new_paper(ctx)
        ret = [{'_id': pid,
                'title': ctx.title,
                'view_cnt': 1,
                'download_cnt': 0
               }]
        ret[0].update(ctx.meta)

        progress_dict[pid] = 0.0
        if len(download_candidates) > 0:
            thread = Thread(target=start_download, args=(download_candidates,
                                                         ctx, pid))
            thread.start()
        return ret
    except:
        log_exc("Failed to save to db")

sp_searcher = SoPaperSearcher()

def handl_author_query(q):
    db = get_mongo('paper')
    res = list(db.find({'author': q}, SEARCH_RETURN_FIELDS))
    return res

def handle_content_query(query):
    log_info("Get content query: {0}".format(query))
    res = sp_searcher.search(query)
    db = get_mongo('paper')

    def transform(r):
        pid = long(r['_id'])
        # XXX should find use '$in' and then do sorting
        doc = db.find_one({'_id': pid}, SEARCH_RETURN_FIELDS)
        if not doc:
            raise Exception("Impossible! Mongo doesn't have this paper in index: {0}".format(pid))
        doc['content'] = r['content']
        doc['weight'] = r['weight']
        return doc

    ret = map(transform, res)
    return ret

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        res = handle_title_query(sys.argv[1])
        sys.exit(0)
    #res = handle_title_query('test test test this is not a paper name')
    #res = handle_title_query('Intriguing properties of neural networks')
    res = handle_content_query('neural networks')
    #res = handle_title_query("The WEka data mining software an update")
    #res = handle_title_query("linear")
    #print res


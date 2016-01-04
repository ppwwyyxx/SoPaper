#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: test-searcher.py
# Date: Tue Jan 20 14:22:43 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from multiprocessing import Pool
import sys

import searcher
from job import JobContext
from searcher import searcher_run

if __name__ == '__main__':
    query = sys.argv[1]
    searchers = searcher.register_searcher.get_searcher_list()
    searchers = searchers[1:]
    print [k.name for k in searchers]
    ctx = JobContext(query)

    args = zip(searchers, [ctx] * len(searchers))
    pool = Pool()
    async_results = [pool.apply_async(searcher_run, arg) for arg in args]

    # Search and get all the results item
    for s in async_results:
        s = s.get()
        if s is None:
            continue
        srs = s['results']

        print srs

        meta = s.get('ctx_update')
        if meta:
            ctx.update_meta_dict(meta)
    pool.close()
    pool.terminate()

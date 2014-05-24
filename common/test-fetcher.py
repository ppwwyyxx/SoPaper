#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: test-fetcher.py
# Date: Sat May 24 20:05:07 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from fetcher import register_parser, SearchResult
from job import JobContext
import ukconfig
from queryhandler import new_paper

import sys

ukconfig.USE_DB = False
ukconfig.USE_INDEXER = False

if __name__ == '__main__':
    if len(sys.argv) == 2:
        ukconfig.USE_DB = True
    ctx = JobContext("Test Filename")

    #parser = register_parser.parser_dict['arxiv.org']
    #sr = SearchResult(None, "http://arxiv.org/abs/1312.6680")
    #sr = SearchResult(None, "  http://arxiv.org/abs/1404.3610")

    #parser = register_parser.parser_dict['dl.acm.org']
    #url = "http://dl.acm.org/citation.cfm?id=1859761"  # twitter
    #url = "http://dl.acm.org/citation.cfm?id=996342"    # SIFT # Large Number of cited
    #url = "http://dl.acm.org/citation.cfm?id=2366157"  # big
    #sr = SearchResult(None, url)

    parser = register_parser.parser_dict['ieeexplore.ieee.org']
    ##sr = SearchResult(None, "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00726791")
    sr = SearchResult(None, "http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4244529")


    params = parser.run(ctx, sr)
    print ctx
    if ukconfig.USE_DB and ctx.success:
        pid = new_paper(ctx)

#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: test-fetcher.py
# Date: Thu Jun 18 23:27:53 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import ukconfig
ukconfig.USE_DB = False
ukconfig.USE_INDEXER = False

from .fetcher import register_parser, SearchResult
from .job import JobContext
from .ukdbconn import new_paper

import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        ukconfig.USE_DB = True
    ctx = JobContext("Test Filename")

    parser = register_parser.parser_dict['arxiv.org']
    sr = SearchResult(None, "http://arxiv.org/abs/1312.6680")
    #sr = SearchResult(None, "  http://arxiv.org/abs/1404.3610")

    #parser = register_parser.parser_dict['dl.acm.org']
    #url = "http://dl.acm.org/citation.cfm?id=1859761"  # twitter
    #url = "http://dl.acm.org/citation.cfm?id=996342"    # SIFT # Large Number of cited
    #url = "http://dl.acm.org/citation.cfm?id=2366157"  # big
    #url = "http://dl.acm.org/citation.cfm?id=1656278"  # Weka
    #sr = SearchResult(None, url)

    #parser = register_parser.parser_dict['ieeexplore.ieee.org']
    #sr = SearchResult(None, "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00726791")
    #sr = SearchResult(None, "http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4244529")


    #parser = register_parser.parser_dict['sciencedirect.com']
    #url = "http://www.sciencedirect.com/science/article/pii/S1570870513000073"
    #sr = SearchResult(None, url)


    #params = parser.fetch_info(ctx, sr)
    #print params
    data = parser.download(sr)

    print(ctx.title)
    if ukconfig.USE_DB and ctx.success:
        pid = new_paper(ctx)

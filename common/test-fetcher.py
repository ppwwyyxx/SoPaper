#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: test-fetcher.py
# Date: Sat May 10 21:48:49 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from fetcher import register_parser, SearchResult
from job import JobContext

if __name__ == '__main__':
    #func = register_parser.parser_dict['arxiv.org']
    #sr = SearchResult(None, "http://arxiv.org/abs/1312.6680")
    #print func(sr)

    parser = register_parser.parser_dict['dl.acm.org']
    url = "http://dl.acm.org/citation.cfm?id=2366157"
    url2 = "http://dl.acm.org/citation.cfm?id=322274"
    sr = SearchResult(None, url)
    ctx = JobContext("Test Filename")
    params = parser.run(ctx, sr)
    print params
    with open('/tmp/a', 'w') as f:
        print >> f, ctx.data

    #func = register_parser.parser_dict['ieeexplore.ieee.org']
    #sr = SearchResult(None, "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00726791")
    #print func(sr)



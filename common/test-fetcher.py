#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: test-fetcher.py
# Date: Sun May 11 00:26:39 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from fetcher import register_parser, SearchResult
from job import JobContext

if __name__ == '__main__':
    ctx = JobContext("Test Filename")

    parser = register_parser.parser_dict['arxiv.org']
    sr = SearchResult(None, "http://arxiv.org/abs/1312.6680")

    #parser = register_parser.parser_dict['dl.acm.org']
    #url = "http://dl.acm.org/citation.cfm?id=2366157"
    #url2 = "http://dl.acm.org/citation.cfm?id=322274"
    #sr = SearchResult(None, url)

    #parser = register_parser.parser_dict['ieeexplore.ieee.org']
    #sr = SearchResult(None, "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00726791")

    params = parser.run(ctx, sr)
    print params


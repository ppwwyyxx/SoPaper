#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: test-fetcher.py
# Date: Sat May 10 19:29:18 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import fetcher
from fetcher import register_parser, SearchResult

if __name__ == '__main__':
    #func = register_parser.parser_dict['arxiv.org']
    #sr = SearchResult(None, "http://arxiv.org/abs/1312.6680")
    #print func(sr)

    #func = register_parser.parser_dict['dl.acm.org']
    #sr = SearchResult(None, "http://dl.acm.org/citation.cfm?id=996342")
    #print func(sr)

    func = register_parser.parser_dict['ieeexplore.ieee.org']
    sr = SearchResult(None, "http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=00726791")
    print func(sr)



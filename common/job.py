#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: job.py
# Date: 一 6月 09 16:29:06 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from lib.textutil import title_beautify
from uklogger import *
from multiprocessing import Pool

class JobContext(object):
    def __init__(self, query):
        self.query = title_beautify(query)
        self.success = False
        self.title = query
        self.existing = None
        self.downloader = []
        self.meta = {}

    def update_meta_dict(self, meta):
        if 'title' in meta:
            del meta['title']
        self.meta.update(meta)

    def need_field(self, fields):
        for f in fields:
            if f not in self.meta:
                return True
        return False

    def add_downloader(self, fetcher_inst):
        self.downloader.append(fetcher_inst)

    def __str__(self):
        d = {'title': self.title,
             'success': self.success,
             'meta': self.meta.keys()
            }
        return str(d)


class SearchResult(object):
    def __init__(self, type, url):
        self.url = url
        self.type = type
        self.searcher = None

    def __str__(self):
        return str(self.searcher) + "; " + \
                str(self.type) + "; " + \
                self.url

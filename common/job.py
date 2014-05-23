#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: job.py
# Date: Fri May 23 20:59:12 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from lib.textutil import title_beautify
from uklogger import *

class JobContext(object):
    def __init__(self, query):
        self.query = title_beautify(query)
        self.success = False
        self.title = query
        self.existing = None
        self.meta = {}

    def update_meta_dict(self, meta):
        self.meta.update(meta)

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

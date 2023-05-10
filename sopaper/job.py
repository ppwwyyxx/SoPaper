#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: job.py
# Date: Thu Jun 18 23:11:07 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from .lib.textutil import title_beautify
from .lib.ukutil import ensure_unicode
from .uklogger import *

class JobContext(object):
    def __init__(self, query):
        query = title_beautify(query)
        self.query = query
        self.success = False
        self.title = query
        self.existing = None
        self.meta = {}

    def update_meta_dict(self, meta):
        if 'title' in meta:
            del meta['title']
        if 'citecnt' not in self.meta and 'citedby' in meta:
            self.meta['citecnt'] = len(meta['citedby'])
        self.meta.update(meta)

    def need_field(self, fields):
        for f in fields:
            if f not in self.meta:
                return True
        return False

    def update_new_title(self, title):
        if title != self.title:
            log_info("Using new title: {0}".format(ensure_unicode(title)))
            self.title = title
            return True
        return False

    def try_update_title_from_search_result(self, s):
        try:
            updated_title = s['ctx_update']['title']
        except KeyError:
            pass
        else:
            self.update_new_title(updated_title)

    def __str__(self):
        d = {'title': self.title,
             'success': self.success,
             'meta': list(self.meta.keys())
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

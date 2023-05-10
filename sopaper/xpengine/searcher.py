#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: searcher.py
# Date: 二 6月 10 04:20:24 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import os
import re

import xappy
from xappy import SearchConnection

from .xpcommon import FIELD_NUM,STOPWORDS

class XapianSearcher(object):

    def __init__(self, dirname):
        self.dbPath = os.path.abspath(dirname)
        self.conn = SearchConnection(self.dbPath)
        # can use 'reopen()' to open the db again

    def reopen(self):
        self.conn.reopen()

    def search(self, query, offset=0, page_size=10, summary_len=300):
        query = self.conn.spell_correct(query)
        words = query.split()
        words = [x for x in words if x not in STOPWORDS]
        query = ' OR '.join(words)
        #query = ' '.join(words)
        q = self.conn.query_field('text', query)

        res = self.conn.search(q, offset * page_size, page_size)

        def transform(r):
            doc = {'_id': r.id,
                    'title': r.data['title'][0],
                    'content': r.summarise('text', maxlen=summary_len),
                    'weight': r.weight
                   }
            return doc

        ret = list(map(transform, res))
        return ret

    def close(self):
        self.conn.close()

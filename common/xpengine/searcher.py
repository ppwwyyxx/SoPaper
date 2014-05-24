#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: searcher.py
# Date: Sat May 24 10:46:59 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import os
import re

import xappy
from xappy import SearchConnection

from xpcommon import FIELD_NUM

class XapianSearcher(object):

    def __init__(self, dirname):
        self.dbPath = os.path.abspath(dirname)
        self.conn = SearchConnection(self.dbPath)
        # can use 'reopen()' to open the db again

    def reopen(self):
        self.conn.reopen()

    def search(self, query, offset=0, page_size=10, summary_len=300):
        query = self.conn.spell_correct(query)
        query = ' OR '.join(query.split())
        q = self.conn.query_field('text', query)

        res = self.conn.search(q, offset * page_size, page_size)

        def transform(r):
            doc = {'_id': r.id,
                    'title': r.data['title'][0],
                    'content': r.summarise('text', maxlen=summary_len)
                   }
            return doc

        ret = map(transform, res)
        return ret

    def close(self):
        self.conn.close()

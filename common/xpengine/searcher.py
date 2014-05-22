#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: searcher.py
# Date: Thu May 22 13:50:35 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import os
import re

import xapian
from xapian import Database, QueryParser, Stem, Enquire

from xpcommon import FIELD_NUM

class XapianSearcher(object):

    def __init__(self, dirname):
        self.dbPath = os.path.abspath(dirname)
        self.db = Database(self.dbPath)

        self.parser = QueryParser()
        self.parser.set_stemmer(Stem('english'))
        self.parser.set_database(self.db)
        self.parser.set_stemming_strategy(QueryParser.STEM_SOME)


    def search(self, query, offset=0, page_size=10):
        parsed_query = self.parser.parse_query(query)

        enquire = Enquire(self.db)
        enquire.set_query(parsed_query)

        matches = enquire.get_mset(offset, page_size)


        def transform(match):
            print "Rank:", match.rank
            doc = match.document
            content = doc.get_data()
            pid = doc.get_value(FIELD_NUM['id'])
            title = doc.get_value(FIELD_NUM['title'])
            return {'id': pid,
                    'title': title,
                    'content': content
                   }

        ret = map(transform, matches)
        return ret




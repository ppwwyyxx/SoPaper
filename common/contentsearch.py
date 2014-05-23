#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: contentsearch.py
# Date: Fri May 23 21:17:39 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import tempfile
import os

from xpengine.indexer import XapianIndexer
from xpengine.searcher import XapianSearcher
import ukconfig
from lib.singleton import Singleton
from ukdbconn import get_mongo
from lib.textutil import filter_nonascii

DB_DIR = ukconfig.XP_DB_DIR

def pdf2text(data):
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    f.write(data)
    f.close()

    os.system('pdftotext "{0}"'.format(f.name))
    fout = f.name.replace('.pdf', '.txt')
    text = open(fout).read()

    os.remove(f.name)
    os.remove(fout)

    text = filter_nonascii(text)
    # TODO filter formulas..
    return text

class SoPaperIndexer(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.indexer = XapianIndexer(DB_DIR)

    def add_paper(self, doc):
        assert doc.get('text')
        assert doc.get('title')
        assert doc.get('id')
        self.indexer.add_doc(doc)
        self.indexer.flush()

    def rebuild(self):
        self.indexer.clear()

        db = get_mongo('paper')
        itr = db.find({}, {'pdf': 1, 'title': 1,
                           'meta.author': 1})
        for res in itr:
            print res.get('meta')
            text = pdf2text(res['pdf'])
            doc = {'text': text,
                   'title': res['title'],
                   'id': res['_id']
                  }
            try:
                author = res['meta']['author']
            except KeyError:
                author = []
            doc['author'] = author
            self.add_paper(doc)
        self.indexer.flush()

class SoPaperSearcher(object):
    """ Search by content of paper """
    __metaclass__ = Singleton

    def __init__(self):
        self.searcher = XapianSearcher(DB_DIR)

    def search(self, query, offset=0,
               page_size=ukconfig.SEARCH_PAGE_SIZE,
               summary_len=ukconfig.SEARCH_SUMMARY_LEN):
        res = self.searcher.search(query, offset, page_size, summary_len)
        return res

sopaper_indexer = SoPaperIndexer()
sopaper_searcher = SoPaperSearcher()

if __name__ == '__main__':
    sopaper_indexer.rebuild()

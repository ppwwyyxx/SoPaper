#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: contentsearch.py
# Date: Sat May 24 00:11:56 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import tempfile
import os
from threading import Lock, Condition

from xpengine.indexer import XapianIndexer
from xpengine.searcher import XapianSearcher
from lib.singleton import Singleton
import ukconfig
from ukdbconn import get_mongo
from lib.textutil import filter_nonascii

DB_DIR = ukconfig.XP_DB_DIR

def pdf2text(data):
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    f.write(data)
    f.close()

    ret = os.system('pdftotext "{0}"'.format(f.name))
    if ret != 0:
        return Exception("pdftotext return error!")
    fout = f.name.replace('.pdf', '.txt')
    text = open(fout).read()

    os.remove(f.name)
    os.remove(fout)

    text = filter_nonascii(text)
    # TODO filter formulas..
    return text

class SoPaperSearcher(object):
    """ Search by content of paper
        Don't instantiate me
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.searcher = XapianSearcher(DB_DIR)

    def search(self, query, offset=0,
               page_size=ukconfig.SEARCH_PAGE_SIZE,
               summary_len=ukconfig.SEARCH_SUMMARY_LEN):
        res = self.searcher.search(query, offset, page_size, summary_len)
        return res

class SoPaperIndexer(object):
    """ Don't instantiate me
    """

    def __init__(self):
        self.indexer = XapianIndexer(DB_DIR)

    def add_paper(self, doc):
        assert doc.get('text')
        assert doc.get('title')
        assert doc.get('id')
        self.indexer.add_doc(doc)
        self.indexer.flush()
        SoPaperSearcher().searcher.reopen()

    def rebuild(self):
        """ should only be called when no searcher is active"""
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
            self.indexer.add_doc(doc)
        self.indexer.flush()

indexer_lock = Lock()
def do_add_paper(doc):
    indexer_lock.acquire()
    idxer = SoPaperIndexer()
    idxer.add_paper(doc)
    SoPaperSearcher().searcher.reopen()
    indexer_lock.release()

if __name__ == '__main__':
    SoPaperIndexer().rebuild()

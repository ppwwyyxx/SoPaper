#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: contentsearch.py
# Date: 五 6月 13 16:55:19 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import tempfile
import os
from threading import Lock, Condition
from lib.timeout import timeout, timeout_command

from xpengine.indexer import XapianIndexer
from xpengine.searcher import XapianSearcher
from lib.singleton import Singleton
import ukconfig
from ukdbconn import get_mongo
from uklogger import *
from lib.textutil import filter_nonascii
from lib.pdfutil import pdf2text

DB_DIR = ukconfig.XP_DB_DIR


class SoPaperSearcher(object):
    """ Search by content of paper
        Don't instantiate me
    """
    __metaclass__ = Singleton

    def __init__(self):
        if not os.path.isdir(DB_DIR):
            SoPaperIndexer().rebuild()
        self.searcher = XapianSearcher(DB_DIR)

    def search(self, query, offset=0,
               page_size=ukconfig.SEARCH_PAGE_SIZE,
               summary_len=ukconfig.SEARCH_SUMMARY_LEN):
        res = self.searcher.search(query, offset, page_size, summary_len)
        return res

class SoPaperIndexer(object):
    """ Don't instantiate me
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.indexer = XapianIndexer(DB_DIR)

    def _do_add_paper(self, doc):
        try:
            self.indexer.add_doc(doc)
        except:
            log_exc("Exception in add_paper")
            log_info("Error with this doc: {0}".format(doc['id']))

    def add_paper(self, doc):
        assert doc.get('text')
        assert doc.get('title')
        assert doc.get('id')
        self._do_add_paper(doc)
        self.indexer.flush()
        SoPaperSearcher().searcher.reopen()

    def rebuild(self):
        self.indexer.clear()

        db = get_mongo('paper')
        itr = db.find({}, {'pdf': 1, 'title': 1, 'text': 1})
        for res in itr:
            text = res.get('text')
            if not text:
                log_info("About to add text for paper {0}".format(res['_id']))
                try:
                    data = res['pdf']
                    text = pdf2text(data)
                except KeyError:
                    log_err("No pdf in pid={0},title={1}".format(
                        res['_id'], res['title']))
                    continue
                except Exception:
                    log_exc("Exception in pdf2text")

                db.update({'_id': res['_id']}, {'$set': {'text': text}})
            doc = {'text': text,
                   'title': res['title'],
                   'id': res['_id']
                  }
            self._do_add_paper(doc)
        self.indexer.flush()

indexer_lock = Lock()
def do_add_paper(doc):
    indexer_lock.acquire()
    idxer = SoPaperIndexer()
    idxer.add_paper(doc)
    SoPaperSearcher().searcher.reopen()
    indexer_lock.release()

if __name__ == '__main__':
    print "Rebuilding..."
    SoPaperIndexer().rebuild()

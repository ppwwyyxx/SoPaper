#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: contentsearch.py
# Date: Fri May 23 12:31:07 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from xpengine.indexer import XapianIndexer
import ukconfig
from lib.singleton import Singleton

DB_DIR = ukconfig.XP_DB_DIR

class SoPaperIndexer(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.indexer = XapianIndexer(DB_DIR)

    def add_paper(self, doc):
        self.indexer.add_doc(doc)
        self.indexer.flush()

    def rebuild(self):
        pass

sopaper_indexer = SoPaperIndexer()

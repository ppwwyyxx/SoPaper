#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: run-xp.py
# Date: Thu May 22 13:50:25 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from indexer import *
from searcher import *

import glob
import os
import sys

db = './xapian-database'

def index():
    indexer = XapianIndexer(db)

    for f in glob.glob('./zbigniew-herbert/*.txt'):
        content = open(f).read()

        doc = {'content': content}
        doc['id'] = '1'
        doc['title'] = os.path.basename(f)
        indexer.add_doc(doc)
    indexer.flush()

def search(query):
    searcher = XapianSearcher(db)
    ret = searcher.search(query)
    print ret

if sys.argv[1] == 'index':
    index()
elif sys.argv[1] == 'search':
    search(sys.argv[2])

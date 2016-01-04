#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: run-xp.py
# Date: Fri May 23 20:19:26 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from indexer import *
from searcher import *

import json
import glob
import os
import sys

db = './xapian-database'

def index():
    indexer = XapianIndexer(db)

    for idx, f in enumerate(glob.glob('./zbigniew-herbert/*.txt')):
        text = open(f).read()

        doc = {'text': text}
        doc['id'] = idx
        doc['title'] = os.path.basename(f)
        doc['author'] = ['Yuxin Wu', 'Angela Doudou']
        indexer.add_doc(doc)
    indexer.flush()

def search(query):
    searcher = XapianSearcher(db)
    ret = searcher.search(query)
    print json.dumps(ret)

if sys.argv[1] == 'index':
    index()
elif sys.argv[1] == 'search':
    search(sys.argv[2])

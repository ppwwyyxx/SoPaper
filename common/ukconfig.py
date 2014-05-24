#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: ukconfig.py
# Date: Sat May 24 17:33:08 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

download_method = 'wget'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

FILE_SIZE_MINIMUM = 10000        # at least 10kb
FILE_SIZE_MAXIMUM = 100000000    # at most 100mb

# this lib is not required for command line script
USE_MAGIC_LIB = False
try:
    import magic
except ImportError:
    USE_MAGIC_LIB = False

USE_DB = True
USE_INDEXER = True
try:
    import pymongo
except ImportError:
    USE_DB = False

mongo_conn = ('127.0.0.1', 27017)
mongo_db = 'sopaper'


import os
DB_DIR_NAME = 'xapian-db'
XP_DB_DIR = os.path.join(os.path.dirname(__file__),
                         '../{0}'.format(DB_DIR_NAME))

SEARCH_PAGE_SIZE = 10
SEARCH_SUMMARY_LEN = 300

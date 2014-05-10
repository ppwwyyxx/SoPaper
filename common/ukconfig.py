#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: ukconfig.py
# Date: Sat May 10 19:57:28 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

#download_method = 'wget'
download_method = 'haha'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

FILE_SIZE_MINIMUM = 10000        # at least 10kb
FILE_SIZE_MAXIMUM = 100000000    # at least 100mb

# this lib not required for command line script
USE_MAGIC_LIB = False
try:
    import magic
except:
    USE_MAGIC_LIB = False

SAVE_TO_FILE = True
SAVE_TO_DB = False

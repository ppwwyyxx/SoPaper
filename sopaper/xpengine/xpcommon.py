#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: xpcommon.py
# Date: Fri May 23 12:35:53 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

FIELD_NUM = {'id': 0,
             'title': 1,
             'text': 2,
             'author': 3
            }

import os

STOPWORDS_FILE = os.path.join(os.path.dirname(__file__), 'stopwords.txt')

STOPWORDS = set([x.strip() for x in open(STOPWORDS_FILE).readlines()])

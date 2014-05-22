#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: xpcommon.py
# Date: Thu May 22 14:27:18 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

FIELD_NUM = {'id': 0,
             'title': 1,
             'text': 2,
             'author': 3
            }

STOPWORDS = set([x.strip() for x in open('./stopwords.txt').readlines()])

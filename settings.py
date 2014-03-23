#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: settings.py
# Date: Mon Mar 24 00:11:47 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

download_method = 'wget'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

title = None

def update_ofile(new_title):
    print "Using new title name: {}".format(new_title)
    global title
    title = new_title

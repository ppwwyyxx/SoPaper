#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: settings.py
# Date: Tue Mar 25 21:15:36 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from text import color_text, title_beautify
download_method = 'wget'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'

title = None

def update_ofile(new_title):
    print color_text("Using new title name: \
                     {}".format(title_beautify(new_title)), 'green')
    global title
    title = new_title

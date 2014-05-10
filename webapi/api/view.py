#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: view.py
# Date: Sat May 10 20:32:58 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import app, redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('static', filename='index.html'))

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: view.py
# Date: Thu May 22 13:14:31 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import app, redirect, url_for, make_response
from flask import render_template
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def nosearch():
    return render_template('search.html')


@app.route('/search/<string:search_word>')
def search():
    res = api.query2(search_word)
    return render_template('search.html',result=res)

    # redirect(url_for('static', filename='search.html'))


@app.route('/api')
def api():
    """ show all the apis"""

    ret = """
api: /download?pid=1

api: /query?q=test

api: /html?pid=2&page=0,1,3,5
0 is the html framework
"""
    ret = ret.strip().replace('\n', '<br/>')
    resp = make_response(ret)
    resp.headers['Content-Type'] = 'text/html'
    return resp

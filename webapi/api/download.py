#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: download.py
# Date: Sat May 10 20:32:13 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import app, make_response, request

# api: /download?pid=1
@app.route('/download')
def download():
    pid = request.values.get('pid')
    data = open("/home/wyx/.vimrc").read()
    resp = make_response(data)
    resp.headers['Content-Disposition'] = "attachment; filename=test space.vimrc"
    return resp

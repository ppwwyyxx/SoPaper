#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: download.py
# Date: Sun May 11 00:33:28 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import app, make_response, request
from ukdbconn import get_mongo

# api: /download?pid=1
@app.route('/download')
def download():
    pid = long(request.values.get('pid'))
    db = get_mongo('paper')

    doc = list(db.find({'_id': pid}).limit(1))
    if not doc:
        return make_response(''), 404
    doc = doc[0]
    data = doc['pdf']
    with open('/tmp/a.pdf', 'w') as f:
        f.write(data)
    resp = make_response(data)
    resp.headers['Content-Disposition'] = "attachment; filename={0}.pdf".format(doc['title'])
    return resp

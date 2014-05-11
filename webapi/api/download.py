#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: download.py
# Date: Sun May 11 14:46:27 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import app, make_response, request
from ukdbconn import get_mongo
from lib.textutil import title_beautify

# api: /download?pid=1
@app.route('/download')
def download():
    pid = long(request.values.get('pid'))
    agent = str(request.user_agent)
    db = get_mongo('paper')


    doc = db.find_and_modify(query={'_id': pid},
                             update={'$inc': {'download_cnt': 1}},
                             fields={'pdf': 1, 'title': 1}
                            )
    title = title_beautify(doc['title'])
    if not doc:
        return make_response(''), 404
    data = doc['pdf']
    resp = make_response(data)
    resp.headers['Content-Type'] = 'application/pdf'


    # chrome doesn't work with comma in filename
    #if agent.find('Chrom') != -1:
        #title = title.replace(',', ' ')

    # TODO deal with unicode name!
    resp.headers['Content-Disposition'] = \
            'attachment; filename="{0}".pdf'.format(title)
    return resp

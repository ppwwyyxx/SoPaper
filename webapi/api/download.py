#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: download.py
# Date: 六 6月 14 03:23:41 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import app, make_response, request, api_method
from ukdbconn import get_mongo
from uklogger import *
from lib.textutil import title_beautify
from queryhandler import progress_dict
from authorfetch import process_fetch_author

# api: /download?pid=1
@app.route('/download')
def download():
    pid = int(request.values.get('pid'))
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
            'attachment; filename="{0}.pdf"'.format(title)
    return resp

# api: /download_available?pid=1
@api_method('/download_available')
def available():
    try:
        pid = int(request.values.get('pid'))
        #log_info("Query available of {0} with dic={1}".
                     #format(pid, str(progress_dict)))
    except:
        return {'status': 'error',
                'reason': 'Invalid Request'}
    prgs = progress_dict.get(pid)
    if prgs is None:
        db = get_mongo('paper')
        doc = db.find_one({'_id': pid}, {'page': 1})
        if not doc:
            return {'status': 'error',
                    'reason': 'no such item'}
        if doc.get('page'):
            doc['progress'] = 'done'
        else:
            doc['progress'] = 'failed'

        doc.update({'status': 'ok'})
        return doc
    return {'status': 'ok',
            'progress': prgs}

# api: /fetchauthor?name=xxx&email=xxx
@api_method('/fetchauthor')
def fetchauthor():
    """ fetch all papers of the author"""
    name = request.values.get('name').lower()
    email = request.values.get('email')

    process_fetch_author(name, email)
    return {'status': 'ok'}

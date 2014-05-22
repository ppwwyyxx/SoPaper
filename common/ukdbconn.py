#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: ukdbconn.py
# Date: Thu May 22 10:43:12 2014 +0800
# Author: jiakai <jia.kai66@gmail.com>
#         Yuxin Wu <ppwwyyxxc@gmail.com>

"""database connections"""


try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient
from pymongo.errors import DuplicateKeyError
from bson.binary import Binary
from threading import Thread

import ukconfig
from uklogger import *
from lib.textutil import title_beautify, parse_file_size
from pdfprocess import pdf_postprocess


_db = None

def get_mongo(coll_name=None):
    global _db
    if _db is None:
        _db = MongoClient(*ukconfig.mongo_conn)[ukconfig.mongo_db]

    if coll_name is None:
        return _db
    return _db[coll_name]


def new_paper(ctx):
    pid = global_counter('paper')
    log_info("Add new paper: {0}, size={1}, pid={2}".format(
        ctx.title, parse_file_size(len(ctx.data)), pid))
    doc = {
        '_id': pid,
        'pdf': Binary(ctx.data),
        'title': ctx.title.lower(),
        'view_cnt': 1,
        'download_cnt': 0
    }
    doc.update(ctx.meta)

    db = get_mongo('paper')
    db.ensure_index('title')
    ret = db.insert(doc)

    thread = Thread(target=pdf_postprocess, args=(ctx.data, pid))
    thread.start()
    return pid

def update_meta(pid, meta):
    db = get_mongo('paper')
    db.update({'_id': pid}, {'$set': meta})

def update_view_cnt(pid):
    db = get_mongo('paper')
    db.update({'_id': pid}, {'$inc': {'view_cnt': 1}})

def global_counter(name, delta=1):
    """ atomically change a global int64 counter and return the newest value;
    starting from 1
    mongo document structure:
    {
        _id: counter name
        val: current value
    }"""
    db = get_mongo('global_counter')
    rst = db.find_and_modify(query={'_id': name},
                            update={'$inc': {'val': delta}},
                            new=True)
    k = rst.get('val')
    if k:
        return k
    try:
        val = long(1)
        db.insert({'_id': name, 'val': val})
        return val
    except DuplicateKeyError:
        return global_counter(name, delta)

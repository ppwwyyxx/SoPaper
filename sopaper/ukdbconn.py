#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: ukdbconn.py
# Date: 二 6月 10 04:01:51 2014 +0000
# Author: jiakai <jia.kai66@gmail.com>
#         Yuxin Wu <ppwwyyxxc@gmail.com>

"""database connections"""


try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient
from pymongo.errors import DuplicateKeyError

from . import ukconfig
from .uklogger import *

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
    log_info("Add new paper: {0}, pid={1}".format(
        ctx.title, pid))
    doc = {
        '_id': pid,
        'title': ctx.title.lower(),
        'view_cnt': 1,
        'download_cnt': 0
    }
    meta = ctx.meta
    if 'author' in meta:
        meta['author'] = [x.lower() for x in meta['author']]
    doc.update(ctx.meta)
    doc['title'] = doc['title'].lower()

    db = get_mongo('paper')
    db.ensure_index('title')
    ret = db.insert(doc)
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
    if rst:
        k = rst.get('val')
        if k:
            return k
    try:
        val = int(1)
        db.insert({'_id': name, 'val': val})
        return val
    except DuplicateKeyError:
        return global_counter(name, delta)

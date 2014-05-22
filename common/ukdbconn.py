#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: ukdbconn.py
# Date: Thu May 22 11:01:02 2014 +0800
# Author: jiakai <jia.kai66@gmail.com>
#         Yuxin Wu <ppwwyyxxc@gmail.com>

"""database connections"""


try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient
from pymongo.errors import DuplicateKeyError

import ukconfig
from uklogger import *

_db = None

def get_mongo(coll_name=None):
    global _db
    if _db is None:
        _db = MongoClient(*ukconfig.mongo_conn)[ukconfig.mongo_db]

    if coll_name is None:
        return _db
    return _db[coll_name]


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

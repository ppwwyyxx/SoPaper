#!./exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: tolower.py
# Date: 二 6月 10 04:03:22 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from pdfprocess import do_addhtml
from ukdbconn import get_mongo

db = get_mongo('paper')
#itr = db.find({'_id': 67L})
itr = db.find({}, {'author': 1, 'title': 1})
for paper in itr:
    try:
        data = paper['author']
    except:
        print(paper['_id'], paper['title'])
        continue
    pid = paper['_id']
    db.update({'_id': pid}, {'$set': {'author': [x.lower() for x in data]}})

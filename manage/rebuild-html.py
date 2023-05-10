#!./exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: rebuild-html.py
# Date: 一 6月 09 17:34:27 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from pdfprocess import do_addhtml
from ukdbconn import get_mongo

db = get_mongo('paper')
itr = db.find({'_id': 67})
for paper in itr:
    try:
        data = paper['pdf']
    except:
        print(paper['_id'], paper['title'])
        continue
    pid = paper['_id']
    do_addhtml(data, pid)

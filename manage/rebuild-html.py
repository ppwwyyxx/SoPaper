#!./exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: rebuild-html.py
# Date: Mon May 26 15:44:09 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from pdfprocess import do_addhtml
from ukdbconn import get_mongo

db = get_mongo('paper')
itr = db.find()
for paper in itr:
    try:
        data = paper['pdf']
    except:
        print paper['_id'], paper['title']
        continue
    pid = paper['_id']
    do_addhtml(data, pid)

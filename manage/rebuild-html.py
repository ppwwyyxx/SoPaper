#!./exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: rebuild-html.py
# Date: Sat May 24 11:43:25 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from pdfprocess import do_addhtml
from ukdbconn import get_mongo

db = get_mongo('paper')
itr = db.find()
for paper in itr:
    data = paper['pdf']
    pid = paper['_id']
    do_addhtml(data, pid)

#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: authorfetch.py
# Date: 五 6月 13 18:06:08 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from collections import defaultdict

from lib.mailutil import sendmail
from ukdbconn import get_mongo

def get_paper_list(name):
    db = get_mongo('paper')
    res = list(db.find({'author': name.lower(), 'pdf': {'$exists': True}},
                       {'title': 1}))
    def transform(r):
        return (r["_id"], r["title"])
    return map(transform, res)

def process_fetch_author(name, email):
    l = get_paper_list(name)
    sendmail(email, name, l)
    print "Mail Sent to {0}".format(email)


if __name__ == '__main__':
    print get_paper_list('jie tang')

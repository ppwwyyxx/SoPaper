#!./exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: dump-db.py
# Date: Sat May 24 11:39:14 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys
import os

from ukdbconn import get_mongo


def dump(pid, output):
    OUTPUT = os.path.join(os.path.dirname(__file__), output)
    pid = int(pid)
    db = get_mongo('paper')

    doc = list(db.find({'_id': pid}).limit(1))[0]
    pdf = doc['pdf']
    title = doc['title']

    try:
        os.mkdir(OUTPUT)
    except:
        pass
    fout = open(os.path.join(OUTPUT, title + '.pdf'), 'w')
    fout.write(pdf)
    fout.close()

    npage = doc.get('page')
    if npage:
        for i in range(npage + 1):
            fout = open(os.path.join(OUTPUT, title + '.html.{0}'.format(i)), 'w')
            fout.write(doc['html'][i])
            fout.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {0} <paper id> <output dir>".format(sys.argv[0]))
        sys.exit()

    dump(sys.argv[1], sys.argv[2])


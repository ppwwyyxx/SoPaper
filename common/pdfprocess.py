#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: pdfprocess.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import tempfile
import os
from bson.binary import Binary

from uklogger import *
from ukdbconn import get_mongo
from lib.pdf2html import PDF2Html
from lib.textutil import parse_file_size
from lib.pdfutil import *
import contentsearch

def do_addhtml(data, pid):
    # convert to html
    converter = PDF2Html(data, filename=None)
    npage = converter.get_npages()
    htmls = [Binary(converter.get(x)) for x in range(npage + 1)]
    converter.clean()

    db = get_mongo('paper')
    db.update({'_id': pid}, {'$set': {'page': npage, 'html': htmls}})
    log_info("Add html for pdf {0}, page={1}".format(pid, npage))

def do_compress(data, pid):
    """ this *must* succeed adding the pdf"""
    try:
        # compress
        data = pdf_compress(data)
    except:
        pass

    db = get_mongo('paper')
    db.update({'_id': pid}, {'$set': {'pdf': Binary(data)}} )
    log_info("Updated pdf {0}: size={1}".format(
        pid, parse_file_size(len(data))))
    return data

def do_buildindex(ctx, data, pid):
    text = pdf2text(data)
    db = get_mongo('paper')
    db.update({'_id': pid}, {'$set': {'text': text}})

    doc = {'text': text,
           'title': ctx.title,
           'id': pid
          }

    citedby = ctx.meta.get('citedby')
    if citedby:
        citecnt = len(citedby)
        doc['citecnt'] = citecnt
    if ctx.meta.get('citecnt'):
        citecnt = ctx.meta.get('citecnt')
        doc['citecnt'] = citecnt

    author = ctx.meta.get('author')
    if author:
        doc['author'] = author
    contentsearch.do_add_paper(doc)

def postprocess(data, ctx, pid):
    """ post-process routine right after adding a new pdf"""
    log_info("Start compressing {0}".format(pid))
    data = do_compress(data, pid)

    try:
        log_info("Start converting to html {0}".format(pid))
        do_addhtml(data, pid)
    except Exception as e:
        log_exc("Error converting to html")

    try:
        log_info("Start converting to text {0}".format(pid))
        do_buildindex(ctx, data, pid)
    except Exception as e:
        log_exc("Error converting to text")

if __name__ == '__main__':
    import sys
    f = sys.argv[1]
    data = open(f).read()

    text = pdf2text(data)
    print text

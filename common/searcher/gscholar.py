#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: gscholar.py
# Date: Sat May 24 20:48:24 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>


from . import register_searcher
from job import SearchResult
from uklogger import *
from lib.textutil import title_correct, filter_title_fileformat, title_beautify

import re
import requests
from bs4 import BeautifulSoup
import urllib
from urlparse import urlparse
import traceback

GOOGLE_SCHOLAR_URL = "http://scholar.google.com/scholar?hl=en&q={0}&btnG=&as_sdt=1%2C5&as_sdtp="

@register_searcher(name='Google Scholar', priority=10)
def search(ctx):
    query = ctx.query.lower()

    ret = {}
    ret['ctx_update'] = {}
    srs = []

    r = requests.get(GOOGLE_SCHOLAR_URL.format(query))
    text = r.text.encode('utf-8')

    soup = BeautifulSoup(text)
    results = soup.findAll(attrs={'class': 'gs_r'})
    title_updated = None
    for rst in results:
        try:
            h3 = rst.findAll('h3')[0]
            real_title = h3.get_text()
            real_title = filter_title_fileformat(real_title)
            if not title_correct(query, real_title):
                continue
            if not title_updated:
                title_updated = title_beautify(real_title)
                log_info("Title updated: {0}".format(title_updated))
                ret['ctx_update']['title'] = title_updated
            url = str(h3.find('a').get('href'))
            srs.append(SearchResult(None, url))

            findpdf = rst.findAll(attrs={'class': 'gs_ggs'})
            if findpdf:
                pdflink = findpdf[0].find('a').get('href')
                url = str(pdflink)
                srs.append(SearchResult('directpdf', url))
        except Exception as e:
            log_exc("Search Item parse error: {0}".format(str(e)))
    ret['results'] = srs
    return ret

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: google.py
# Date: 一 6月 09 13:31:04 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_searcher
from job import SearchResult
from uklogger import *
from lib.textutil import title_correct, filter_title_fileformat
import ukconfig

import re
import urllib
from bs4 import BeautifulSoup
from urlparse import urlparse
import traceback
import requests

GOOGLE_URL = "http://www.google.com.hk/search?q={0}"

def parse_google_link(url):
    real = re.findall('http[^&]*&', url)[0]
    ret = urllib.unquote(real[:-1])
    return ret

@register_searcher(name='Google')
def search(ctx):
    query = ctx.query.lower()

    ret = {}
    ret['ctx_update'] = {}
    srs = []

    headers = { 'Hostname': 'www.google.com',
                'User-Agent': ukconfig.USER_AGENT}
    r = requests.get(GOOGLE_URL.format(query), headers=headers, verify=False)
    text = r.text.encode('utf-8')
    with open('/tmp/a.html', 'w') as f:
        print >> f, text

    def find_citecnt(dom):
        try:
            find = dom.findAll(attrs={'class': 'f slp'})[0]
            find = find.findAll('a')[0].text
            citecnt = re.search('[0-9]+', find).group()
            return int(citecnt)
        except:
            return None

    soup = BeautifulSoup(text)
    results = soup.findAll(attrs={'class': 'g'})
    for rst in results:
        try:
            h3 = rst.findAll('h3')[0]
            real_title = h3.get_text()
            if not title_correct(query, real_title):
                continue
            # TODO do some title update?
            cnt = find_citecnt(rst)
            if cnt:
                ret['ctx_update']['citecnt'] = cnt
            findpdf = rst.findAll(attrs={'class': 'mime'})
            if findpdf and findpdf[0].text == '[PDF]':
                pdflink = rst.findAll('a')[0].get('href')
                try:
                    url = parse_google_link(pdflink)
                except:
                    continue
                srs.append(SearchResult('directpdf', url))
            else:
                url = rst.findAll('a')[0].get('href')
                try:
                    url = parse_google_link(url)
                except:
                    continue
                srs.append(SearchResult(None, url))
        except Exception as e:
            log_exc("Search Item parse error: {0}".format(str(e)))
    ret['results'] = srs
    return ret

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: google.py
# Date: Wed Mar 11 09:21:06 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_searcher
from ..job import SearchResult
from ..uklogger import *
from ..lib.textutil import title_correct, filter_title_fileformat
from ..ukconfig import BS_PARSER

import re
import urllib
from bs4 import BeautifulSoup
from urlparse import urlparse
import traceback
import requests

GOOGLE_URL = "https://www.google.com/search?q={0}"

def parse_google_link(url):
    return url      # now it seems to be ok
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
                'User-Agent': ukconfig.USER_AGENT,
                'Accept-Encoding': 'gzip'
              }
    r = requests.get(GOOGLE_URL.format(query), headers=headers, verify=True)
    text = r.text.encode('utf-8')
    #with open('/tmp/a.html', 'r') as f:
        ##f.write(text)
        #text = f.read()

    def find_citecnt(dom):
        try:
            find = dom.findAll(attrs={'class': 'f slp'})[0]
            find = find.findAll('a')[0].text
            citecnt = re.search('[0-9]+', find).group()
            return int(citecnt)
        except:
            return None

    soup = BeautifulSoup(text, BS_PARSER)
    results = soup.findAll(attrs={'class': 'g'})
    for rst in results:
        try:
            h3 = rst.findAll('h3')
            if not h3:  # frame search, e.g. picture/video/kg
                continue
            real_title = h3[0].get_text()
            tc = title_correct(query, real_title)
            if not tc[0]:
                continue
            # TODO do some title update?
            cnt = find_citecnt(rst)
            if cnt is not None:
                ret['ctx_update']['citecnt'] = cnt
            #findpdf = rst.findAll(attrs={'class': 'mime'})
            findpdf = rst.findAll('span')
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

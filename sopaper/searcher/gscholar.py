#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: gscholar.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>


from . import register_searcher
from ..job import SearchResult
from ..uklogger import *
from ..lib.textutil import title_correct, filter_title_fileformat, title_beautify
from ..lib.ukutil import ensure_unicode, ensure_bin_str
from ..ukconfig import BS_PARSER

import re
import requests
from bs4 import BeautifulSoup
import urllib
from urlparse import urlparse
import traceback

GOOGLE_SCHOLAR_URL = "https://scholar.google.com/scholar?hl=en&q={0}&btnG=&as_sdt=1%2C5&as_sdtp="

@register_searcher(name='Google Scholar', priority=10)
def search(ctx):
    query = ctx.query.lower()

    ret = {}
    ret['ctx_update'] = {}
    srs = []

    r = requests.get(GOOGLE_SCHOLAR_URL.format(query))
    text = r.text.encode('utf-8')
    #with open('/tmp/b.html', 'r') as f:
        #text = f.read()

    def find_citecnt(dom):
        try:
            find = dom.findAll(attrs={'class': 'gs_ri'})[0]
            find = find.findAll(attrs={'class': 'gs_fl'})[0]
            find = find.findAll('a')[0].text
            cnt = re.search('[0-9]+', find).group()
            return int(cnt)
        except:
            return None


    soup = BeautifulSoup(text, BS_PARSER)
    results = soup.findAll(attrs={'class': 'gs_r'})
    title_updated = None
    for rst in results:
        try:
            h3 = rst.findAll('h3')[0]
            real_title = h3.get_text()
            real_title = filter_title_fileformat(real_title)
            tc = title_correct(query, real_title)
            if not tc[0]:
                continue
            if not title_updated and tc[1]:
                title_updated = ensure_unicode(title_beautify(real_title))
                while True:     # fix things like '[citation][c] Title'
                    new_title = re.sub('^\[[^\]]*\]', '', title_updated).strip()
                    if new_title == title_updated:
                        title_updated = new_title
                        break
                    title_updated = new_title
                log_info(u"Title updated: {0}".format(title_updated))
                ret['ctx_update']['title'] = title_updated

            cnt = find_citecnt(rst)
            if cnt is not None:
                ret['ctx_update']['citecnt'] = cnt

            try:
                url = str(h3.find('a').get('href'))
                srs.append(SearchResult(None, url))
            except:
                pass

            findpdf = rst.findAll(attrs={'class': 'gs_ggs'})
            if findpdf:
                pdflink = findpdf[0].find('a').get('href')
                url = str(pdflink)
                srs.append(SearchResult('directpdf', url))
        except Exception as e:
            log_exc("Search Item parse error: {0}".format(str(e)))
    ret['results'] = srs
    return ret

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: arxiv.py
# Date: Thu May 22 11:13:05 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
from uklogger import *
import re
from bs4 import BeautifulSoup
import requests

ARXIV_PAT = re.compile('arxiv\.org/[^/]*/(?P<id>.*)')

@register_parser(name='arxiv.org', urlmatch='arxiv.org')
def arxiv(search_result):
    url = search_result.url
    ret = {}
    meta = {}

    try:
        match = ARXIV_PAT.search(url).groupdict()
        pid = match['id']
        pdflink = "http://arxiv.org/pdf/{0}.pdf".format(pid)
        ret['url'] = pdflink
    except:
        pass

    text = requests.get(url).text.encode('utf-8')
    soup = BeautifulSoup(text)

    try:
        title = soup.findAll(attrs={'name': 'citation_title'})[0]
        title = title.get('content')
        meta['title'] = title
    except:
        pass

    try:
        authors = soup.findAll(attrs={'class': 'authors'})[0]
        authors = authors.findAll('a')
        author = [a.text for a in authors]
        meta['author'] = author
    except:
        pass

    try:
        abstract = soup.findAll(attrs={'class': 'abstract mathjax'})[0]
        abstract = abstract.text.strip()
        abstract = abstract[abstract.find(':')+1:].strip()
        meta['abstract'] = abstract
    except:
        pass

    try:
        bibtex_url = soup.findAll(attrs={'title': 'DBLP bibtex record'})
        bibtex_url = bibtex_url[0].get('href')
        bibtex_text = requests.get(bibtex_url).text.encode('utf-8')
        bibtex_soup = BeautifulSoup(bibtex_text)
        pre = bibtex_soup.findAll('pre')[0]
        bibtex = pre.text
        meta['bibtex'] = bibtex
    except:
        pass

    if not ret.get('bibtex') or not ret.get('author') \
       or not ret.get('abstract') or not ret.get('title'):
        log_info('Missing metadata in {0}'.format(search_result.url))

    ret['ctx_update'] = meta
    return ret

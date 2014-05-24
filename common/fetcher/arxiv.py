#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: arxiv.py
# Date: Sat May 24 15:57:18 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
from .base import FetcherBase, direct_download
from uklogger import *
import re
from bs4 import BeautifulSoup
import requests

ARXIV_PAT = re.compile('arxiv\.org/[^/]*/(?P<id>.*)')

@register_parser(name='arxiv.org', urlmatch='arxiv.org')
class Arxiv(FetcherBase):
    def _do_pre_parse(self):
        text = requests.get(self.url).text.encode('utf-8')
        self.soup = BeautifulSoup(text)

    def _do_download(self, updater):
        match = ARXIV_PAT.search(self.url).groupdict()
        pid = match['id']
        pdflink = "http://arxiv.org/pdf/{0}.pdf".format(pid)
        return direct_download(pdflink, updater)

    def _do_get_title(self):
        title = self.soup.findAll(attrs={'name': 'citation_title'})[0]
        title = title.get('content')
        return title

    def _do_get_meta(self):
        meta = {}
        try:
            authors = self.soup.findAll(attrs={'class': 'authors'})[0]
            authors = authors.findAll('a')
            author = [a.text for a in authors]
            meta['author'] = author
        except:
            pass

        try:
            abstract = self.soup.findAll(attrs={'class': 'abstract mathjax'})[0]
            abstract = abstract.text.strip()
            abstract = abstract[abstract.find(':')+1:].strip()
            meta['abstract'] = abstract
        except:
            pass

        try:
            bibtex_url = self.soup.findAll(attrs={'title': 'DBLP bibtex record'})
            bibtex_url = bibtex_url[0].get('href')
            bibtex_text = requests.get(bibtex_url).text.encode('utf-8')
            bibtex_soup = BeautifulSoup(bibtex_text)
            pre = bibtex_soup.findAll('pre')[0]
            bibtex = pre.text
            meta['bibtex'] = bibtex
        except:
            pass
        return meta

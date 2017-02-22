#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: arxiv.py
# Date: Thu Jun 18 23:32:54 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
from .base import FetcherBase, direct_download
from ..uklogger import *
from ..ukconfig import BS_PARSER

import re
from bs4 import BeautifulSoup
import requests

#ARXIV_PAT = re.compile('arxiv\.org/[^/]*/(?P<id>.*)')

@register_parser(name='arxiv.org', urlmatch='arxiv.org',
                meta_field=['author', 'bibtex', 'abstract'],
                priority=7)
class Arxiv(FetcherBase):
    def _do_pre_parse(self):
        if 'pdf' in self.url:   # change /pdf/xxx.xxx to /abs/xxx.xxx
            self.url = self.url.replace('pdf', 'abs')
            if self.url.endswith('.abs'):
                self.url = self.url[:-4]
        text = requests.get(self.url).text.encode('utf-8')
        self.soup = BeautifulSoup(text, BS_PARSER)

    def _do_download(self, updater):
        full_text_div = self.soup.findAll('div', attrs={'class': 'full-text'})[0]
        link = full_text_div.findAll('li')[0]
        partial_link = link.children.next().get('href')

        prefix = 'http://arxiv.org'
        if 'cn.arxiv.org' in self.url:  # handle cn.arxiv
            prefix = 'http://cn.arxiv.org'
        return direct_download(prefix + partial_link, updater)

        #match = ARXIV_PAT.search(self.url).groupdict()
        #pid = match['id']
        #pdflink = "http://arxiv.org/pdf/{0}.pdf".format(pid)
        #return direct_download(pdflink, updater)

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
            bibtex_soup = BeautifulSoup(bibtex_text, BS_PARSER)
            pre = bibtex_soup.findAll('pre')[0]
            bibtex = pre.text
            meta['bibtex'] = bibtex
        except:
            pass
        return meta

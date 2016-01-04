#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: ieee.py
# Date: 五 6月 13 18:22:19 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
from .base import FetcherBase, direct_download
from ..uklogger import *
from ..ukconfig import BS_PARSER

import re
from bs4 import BeautifulSoup
import requests

HOSTNAME = 'ieeexplore.ieee.org'
STAMP_URL = "http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={0}"
REFERENCE_URL = "http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?tp=&arnumber={0}"
CITATION_URL = "http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?tp=&arnumber={0}"

@register_parser(name='ieeexplore.ieee.org',
                 urlmatch='ieeexplore.ieee.org',
                 meta_field=['author', 'abstract', 'references', 'citedby'])
class IEEE(FetcherBase):
    def _do_pre_parse(self):
        text = requests.get(self.url).text.encode('utf-8')
        self.soup = BeautifulSoup(text, BS_PARSER)

        number = re.findall('arnumber=[0-9]*', self.url)[0]
        self.number = re.findall('[0-9]+', number)[0]

    def _do_download(self, updater):
        url2 = STAMP_URL.format(self.number)
        text = requests.get(url2).text.encode('utf-8')
        soup = BeautifulSoup(text, BS_PARSER)
        fr = soup.findAll('frame')[-1]
        pdflink = fr.get('src')
        return direct_download(pdflink, updater)

    def _do_get_title(self):
        titles = self.soup.findAll('h1')
        title = titles[0].text.strip()
        return title

    def _do_get_meta(self):
        meta = {}
        try:
            authors = self.soup.findAll(attrs={'name': 'citation_author'})
            author = [a.get('content') for a in authors]
            meta['author'] = author
        except KeyboardInterrupt:
            raise
        except:
            pass

        try:
            abstract_div = self.soup.findAll(attrs={'class': 'article'})
            abstract = abstract_div[0].text.strip()
            meta['abstract'] = abstract
        except KeyboardInterrupt:
            raise
        except:
            pass

        try:
            ref_url = REFERENCE_URL.format(self.number)
            ref_text = requests.get(ref_url).text
            ref_soup = BeautifulSoup(ref_text, BS_PARSER)
            ol = ref_soup.findAll('ol')[0]
            lis = ol.findAll('li')
            reference = []
            for li in lis:
                ref = li.text.strip()
                ref = ref.replace('\t', '')
                ref = ref.replace('\n', '')
                ref = ref.replace('\r', '')
                ref = ref.replace('\\', '')
                ref = ref.replace(u'\xa0', u' ')
                if 'Abstract' in ref:
                    ref = ref[:ref.find('Abstract')]
                if 'Cross' in ref:
                    ref = ref[:ref.find('[')]
                href = ''
                link = li.findAll('a')
                if len(link) > 0:
                    href = link[0].get('href')
                    if not 'http' in href:
                        href = "http://{0}{1}".format(HOSTNAME, href)
                reference.append({'ref': ref, 'href': href})
            meta['references'] = reference
        except KeyboardInterrupt:
            raise
        except:
            pass

        try:
            cite_url = CITATION_URL.format(self.number)
            cite_text = requests.get(cite_url).text.encode('utf-8')
            cite_soup = BeautifulSoup(cite_text, BS_PARSER)
            html = cite_soup.findAll('ol')[0]
            lis = html.findAll('li')
            citing = []
            for li in lis:
                cite = li.text.strip()
                cite = cite.replace('\t', '')
                cite = cite.replace('\n', '')
                cite = cite.replace('\r', '')
                cite = cite.replace('\\', '')
                cite = cite.replace('  ', '')
                cite = cite.replace(u'\xa0', u' ')
                if 'Abstract' in cite:
                    cite = cite[:cite.find('Abstract')]
                if 'Cross' in cite:
                    cite = cite[:cite.find('[')]
                href = ''
                link = li.findAll('a')
                if len(link) > 0:
                    href = "http://{0}{1}".format(HOSTNAME,
                        re.findall(r'/xpl/articleDetails.jsp\?arnumber=[0-9]+', link[0].get('href'))[0])
                citing.append({'citing': cite, 'href': href})
            meta['citedby'] = citing
        except KeyboardInterrupt:
            raise
        except:
            pass

        """
        there are still difficulties getting the bibtex
        """

        return meta

#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: dlacm.py
# Date: Thu Jun 25 16:33:15 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import re
from . import register_parser, RecoverableErr
from .base import FetcherBase
from ..lib.downloader import wget_download
from ..uklogger import *
from .. import ukconfig
from ..ukconfig import BS_PARSER

from urlparse import urlparse
import requests
from bs4 import BeautifulSoup

HOSTNAME = 'dl.acm.org'
DEFAULT_TIMEOUT = '300.0'   # 5 minutes

# Bug in requests:
# requests would fail to download paper from dl.acm.org. use wget instead
def download(url, updater):
    log_info("Custom Directly Download with URL {0} ...".format(url))
    headers = {'Host': urlparse(url).netloc,
               'User-Agent': ukconfig.USER_AGENT,
               'Connection': 'Keep-Alive'
              }

    resp = requests.get(url, headers=headers, allow_redirects=False)
    pdfurl = resp.headers.get('location')
    if pdfurl:
        headers['Host'] = urlparse(pdfurl).netloc
        return wget_download(pdfurl, updater, headers)
    else:
        return wget_download(url, updater)

@register_parser(name='dl.acm.org', urlmatch='dl.acm.org',
                 meta_field=['author', 'bibtex', 'citedby', 'references',
                             'abstract'],
                 priority=2)
class DLAcm(FetcherBase):
    def _do_pre_parse(self):
        self.text = requests.get(self.url).text.encode('utf-8')
        #with open("/tmp/b.html", 'w') as f:
            #f.write(self.text)
        #text = open("/tmp/b.html").read()
        self.soup = BeautifulSoup(self.text, BS_PARSER)

    def _do_download(self, updater):
        pdf = self.soup.findAll(attrs={'name': 'FullTextPDF'})
        if not pdf:
            pdf = self.soup.findAll(attrs={'name': 'FullTextPdf'})
        if pdf:
            try:
                url = pdf[0].get('href')
                url = 'http://{0}/'.format(HOSTNAME) + url
                log_info("dl.acm origin url: {0}".format(url))
                r = requests.get(url, allow_redirects=False)
                pdfurl = r.headers.get('location')
            except:
                # probably something need to be fixed
                log_exc('')
        else:
            raise RecoverableErr("dl.acm has no available download at {0}".format(self.url))
        return download(pdfurl, updater)

    def _do_get_title(self):
        titles = self.soup.findAll(attrs={'name': 'citation_title'})
        return titles[0]['content']

    def _do_get_meta(self):
        meta = {}
        try:
            log_info("Getting author...")
            authors = self.soup.findAll(
                attrs={'title': 'Author Profile Page'})
            author = [a.text for a in authors]
            meta['author'] = author
        except KeyboardInterrupt:
            raise
        except:
            pass

        try:
            log_info("Getting abstract...")
            abstract_url = re.findall(r'\'tab_abstract.+\d+\'', self.text)[0][1:-1]
            abstract_text = requests.get('http://{0}/'.format(HOSTNAME) + abstract_url).text.encode('utf-8')
            abstract_soup = BeautifulSoup(abstract_text, BS_PARSER)
            abstract = abstract_soup.findAll('p')[0].text
            meta['abstract'] = abstract
        except KeyboardInterrupt:
            raise
        except:
            pass

        try:
            log_info("Getting refs ...")
            ref_url = re.findall(r'\'tab_references.+\d+\'', self.text)[0][1:-1]
            ref_text = requests.get('http://{0}/'.format(HOSTNAME) + ref_url).text.encode('utf-8')
            ref_soup = BeautifulSoup(ref_text, BS_PARSER)
            trs = ref_soup.findAll('tr')
            reference = []
            for tr in trs:
                records = tr.findAll('a')
                if len(records) > 0:
                    href = 'http://{0}/'.format(HOSTNAME) + records[0].get('href')
                    ref = records[0].text.strip()
                    reference.append({'ref': ref, 'href': href})
            meta['references'] = reference
        except KeyboardInterrupt:
            raise
        except:
            pass

        try:
            log_info("Getting cited ...")
            cite_url = re.findall(r'\'tab_citings.+\d+\'', self.text)[0][1:-1]
            cite_text = requests.get('http://{0}/'.format(HOSTNAME) +
                                     cite_url, timeout=5
                                    ).text.encode('utf-8')
            cite_soup = BeautifulSoup(cite_text, BS_PARSER)
            trs = cite_soup.findAll('tr')
            citing = []
            for tr in trs:
                records = tr.findAll('a')
                if len(records) > 0:
                    href = 'http://{0}/'.format(HOSTNAME) + records[0].get('href')
                    cite = records[0].text.strip()
                    citing.append({'citing': cite, 'href': href})
            meta['citedby'] = citing
        except KeyboardInterrupt:
            raise
        except requests.exceptions.Timeout:
            pass
        except:
            pass

        try:
            log_info("Getting bibtex...")
            bibtex_url = re.findall(r'exportformats.+bibtex', self.text)[0]
            bibtex_text = requests.get('http://{0}/'.format(HOSTNAME) + bibtex_url).text.encode('utf-8')
            bibtex_soup = BeautifulSoup(bibtex_text, BS_PARSER)
            pre = bibtex_soup.find('pre')
            bibtex = pre.text.strip()
            meta['bibtex'] = bibtex
        except KeyboardInterrupt:
            raise
        except:
            pass
        return meta

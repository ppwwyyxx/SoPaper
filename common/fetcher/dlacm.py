#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dlacm.py
# Date: Sun May 25 19:37:54 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import re
from . import register_parser, RecoverableErr
from .base import FetcherBase
from uklogger import *
import ukconfig
from lib.textutil import parse_file_size

from urlparse import urlparse
import requests
import human_curl
#from human_curl.exceptions import CurlError
from bs4 import BeautifulSoup

HOSTNAME = 'dl.acm.org'
DEFAULT_TIMEOUT = '300'   # 5 minutes

# Bug in requests:
# To download paper from dl.acm.org, human_curl must be used instead of requests
# Seem unable to support streaming download with human_curl
def download(url, updater):
    log_info("Custom Directly Download with URL {0} ...".format(url))
    headers = {'Host': urlparse(url).netloc,
               'User-Agent': ukconfig.USER_AGENT,
               'Connection': 'Keep-Alive'
              }
    resp = human_curl.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
    try:
        total_length = int(resp.headers.get('content-length'))
    except:
        pdfurl = resp.headers.get('location')
        return download(pdfurl, updater)

    log_info("dl.acm.org: filesize={0}".format(parse_file_size(total_length)))
    if total_length < ukconfig.FILE_SIZE_MINIMUM:
        raise RecoverableErr("File too small: " + parse_file_size(total_length))
    if total_length > ukconfig.FILE_SIZE_MAXIMUM:
        raise RecoverableErr("File too large: " + parse_file_size(total_length))
    data = resp.content
    updater.finish(data)
    return data

@register_parser(name='dl.acm.org', urlmatch='dl.acm.org',
                 meta_field=['author', 'bibtex', 'citedby', 'references', 'abstract'])
class DLAcm(FetcherBase):
    def _do_pre_parse(self):
        self.text = requests.get(self.url).text.encode('utf-8')
        #with open("/tmp/b.html", 'w') as f:
            #f.write(self.text)
        #text = open("/tmp/b.html").read()
        self.soup = BeautifulSoup(self.text)

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
            abstract_soup = BeautifulSoup(abstract_text)
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
            ref_soup = BeautifulSoup(ref_text)
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
            cite_soup = BeautifulSoup(cite_text)
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
            bibtex_soup = BeautifulSoup(bibtex_text)
            pre = bibtex_soup.find('pre')
            bibtex = pre.text.strip()
            meta['bibtex'] = bibtex
        except KeyboardInterrupt:
            raise
        except:
            pass
        return meta

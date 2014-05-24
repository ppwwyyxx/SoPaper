#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dlacm.py
# Date: Sat May 24 10:57:57 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import re
from . import register_parser, RecoverableErr
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
def download(res, updater):
    url = res['url']
    log_info("Custom Directly Download with URL {0} ...".format(url))
    headers = {'Host': urlparse(url).netloc,
               'User-Agent': ukconfig.USER_AGENT,
               'Connection': 'Keep-Alive'
              }
    resp = human_curl.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
    total_length = int(resp.headers.get('content-length'))
    log_info("dl.acm.org: filesize={0}".format(parse_file_size(total_length)))
    if total_length < ukconfig.FILE_SIZE_MINIMUM:
        with open("/tmp/a.txt", 'w') as f:
            f.write(resp.content)
        raise RecoverableErr("File too small: " + parse_file_size(total_length))
    if total_length > ukconfig.FILE_SIZE_MAXIMUM:
        raise RecoverableErr("File too large: " + parse_file_size(total_length))
    data = resp.content
    updater.finish()
    return data

@register_parser(name='dl.acm.org', urlmatch='dl.acm.org',
                 custom_downloader=download)
def dlacm(search_result):
    url = search_result.url
    ret = {}
    meta = {}

    text = requests.get(url).text.encode('utf-8')
    #with open("/tmp/b.html", 'w') as f:
        #f.write(text)
    #text = open("/tmp/b.html").read()
    soup = BeautifulSoup(text)
    pdf = soup.findAll(attrs={'name': 'FullTextPDF'})
    if pdf:
        try:
            url = pdf[0].get('href')
            url = 'http://{0}/'.format(HOSTNAME) + url
            log_info("dl.acm origin url: {0}".format(url))
            r = requests.get(url, allow_redirects=False)
            pdfurl = r.headers.get('location')
            r = requests.get(pdfurl, allow_redirects=False)
            pdfurl = r.headers.get('location')
            ret['url'] = pdfurl
        except:
            # probably something need to be fixed
            log_exc('')

    titles = soup.findAll('title')
    title = titles[0].text

    try:
        authors = soup.findAll(
            attrs={'title': 'Author Profile Page'})
        author = [a.text for a in authors]
        meta['author'] = author
    except:
        pass

    try:
        abstract_url = re.findall(r'\'tab_abstract.+\d+\'', text)[0][1:-1]
        abstract_text = requests.get('http://{0}/'.format(HOSTNAME) + abstract_url).text.encode('utf-8')
        abstract_soup = BeautifulSoup(abstract_text)
        abstract = abstract_soup.findAll('p')[0].text
        meta['abstract'] = abstract
    except:
        pass

    try:
        ref_url = re.findall(r'\'tab_references.+\d+\'', text)[0][1:-1]
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
    except:
        pass

    try:
        cite_url = re.findall(r'\'tab_citings.+\d+\'', text)[0][1:-1]
        cite_text = requests.get('http://{0}/'.format(HOSTNAME) + cite_url).text.encode('utf-8')
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
    except:
        pass

    try:
        bibtex_url = re.findall(r'exportformats.+bibtex', text)[0]
        bibtex_text = requests.get('http://{0}/'.format(HOSTNAME) + bibtex_url).text.encode('utf-8')
        bibtex_soup = BeautifulSoup(bibtex_text)
        pre = bibtex_soup.find('pre')
        bibtex = pre.text.strip()
        meta['bibtex'] = bibtex
    except:
        pass

    if not ret.get('bibtex') or not ret.get('citedby') \
       or not ret.get('author') or not ret.get('references') \
       or not ret.get('abstract'):
        log_info('missing metadata in {0}'.format(search_result.url))

    ret['ctx_update'] = meta
    return ret

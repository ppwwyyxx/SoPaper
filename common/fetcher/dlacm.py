#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dlacm.py
# Date: Sat May 10 19:28:36 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
import requests
from bs4 import BeautifulSoup
from uklogger import log_info

HOSTNAME = 'dl.acm.org'

@register_parser(name='dl.acm.org', urlmatch='dl.acm.org')
def dlacm(search_result):
    url = search_result.url

    text = requests.get(url).text.encode('utf-8')

    #with open("/tmp/b.html", 'w') as f:
        #f.write(text)
    #text = open("/tmp/b.html").read()
    soup = BeautifulSoup(text)
    pdf = soup.findAll(attrs={'name': 'FullTextPDF'})
    if not pdf:
        return
    url = pdf[0].get('href')
    url = 'http://{0}/'.format(HOSTNAME) + url
    log_info("dl.acm origin url: {0}".format(url))

    r = requests.get(url, allow_redirects=False)
    url = r.headers.get('location')
    if url.find('pdf') != -1:
        return {'url': url}

    r = requests.get(url, allow_redirects=False)
    url = r.headers.get('location')
    if url.find('pdf') != -1:
        return {'url': url}


#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: handlers.py
# Date: Thu Mar 13 23:44:00 2014 +0800

import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36'

def dl_acm_org(link):
    HOSTNAME = 'dl.acm.org'
    if link.netloc != HOSTNAME:
        return None
    url = link.geturl()

    #text = requests.get(url).text.encode('utf-8')
    text = open("/tmp/b.html").read()

    soup = BeautifulSoup(text)
    #try:
    pdf = soup.findAll(attrs={'name': 'FullTextPDF'})
    url = pdf[0].get('href')
    url = 'http://{0}/'.format(HOSTNAME) + url
    print url
    r = requests.get(url, headers={'Host': HOSTNAME,
                                   'User-Agent': USER_AGENT,
                                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})
    print r
    print r.headers.get('location')
    #except:
        #return None


if __name__ == '__main__':
    dl_acm_org('dl.acm.org/citation.cfm?id=2461993')

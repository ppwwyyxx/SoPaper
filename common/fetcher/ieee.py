#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: ieee.py
# Date: Thu May 22 11:15:25 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
from uklogger import *

import re
from bs4 import BeautifulSoup
import requests

HOSTNAME = 'ieeexplore.ieee.org'
STAMP_URL = "http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={0}"
REFERENCE_URL = "http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?tp=&arnumber={0}"
CITATION_URL = "http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?tp=&arnumber={0}"

@register_parser(name='ieeexplore.ieee.org',urlmatch='ieeexplore.ieee.org')
def ieee(search_result):
    url = search_result.url
    ret = {}
    meta = {}

    try:
        number = re.findall('arnumber=[0-9]*', url)[0]
        number = re.findall('[0-9]+', number)[0]
        url2 = STAMP_URL.format(number)
        text = requests.get(url2).text.encode('utf-8')
        soup = BeautifulSoup(text)
        fr = soup.findAll('frame')[-1]
        pdflink = fr.get('src')
        ret['url'] = pdflink
    except:
        pass

    try:
        text = requests.get(url).text.encode('utf-8')
        soup = BeautifulSoup(text)
        titles = soup.findAll('h1')
        title = titles[0].text.strip()
        meta['title'] = title
    except:
        pass

    try:
        authors = soup.findAll(attrs={'name': 'citation_author'})
        author = [a.get('content') for a in authors]
        meta['author'] = author
    except:
        pass

    try:
        abstract_div = soup.findAll(attrs={'class': 'article'})
        abstract = abstract_div[0].text.strip()
        meta['abstract'] = abstract
    except:
        pass

    try:
        ref_url = REFERENCE_URL.format(number)
        ref_text = requests.get(ref_url).text
        ref_soup = BeautifulSoup(ref_text)
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
    except:
        pass

    try:
        cite_url = CITATION_URL.format(number)
        cite_text = requests.get(cite_url).text.encode('utf-8')
        cite_soup = BeautifulSoup(cite_text)
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
    except:
        pass

    """
    there are still difficulties getting the bibtex
    """

    if not ret.get('bibtex') or not ret.get('citedby') \
       or not ret.get('author') or not ret.get('references') \
       or not ret.get('abstract'):
        log_info('Missing metadata in {0}'.format(search_result.url))

    ret['ctx_update'] = meta
    return ret

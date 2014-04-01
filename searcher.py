#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: searcher.py
# Date: Tue Apr 01 14:48:53 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from resources.resource import DirectPDFResource


import re
import requests
from text import title_correct, color_text
from bs4 import BeautifulSoup
import urllib
from urlparse import urlparse
import traceback
import settings

class Searcher(object):
    def __init__(self):
        pass

    def search(self, query):
        """ return a list of DirectPDFResource or string"""
        pass

class ScholarSearcher(Searcher):
    GOOGLE_SCHOLAR_URL = "http://scholar.google.com/scholar?hl=en&q={0}&btnG=&as_sdt=1%2C5&as_sdtp="

    def __init__(self):
        self.name = "Google Scholar"

    def search(self, query):
        ret = []

        r = requests.get(ScholarSearcher.GOOGLE_SCHOLAR_URL.format(query))
        text = r.text.encode('utf-8')

        soup = BeautifulSoup(text)
        results = soup.findAll(attrs={'class': 'gs_r'})
        title_updated = False
        for rst in results:
            try:
                h3 = rst.findAll('h3')[0]
                real_title = h3.get_text()
                if not title_correct(query, real_title):
                    continue
                if not title_updated:
                    settings.update_ofile(real_title)
                    title_updated = True
                url = h3.find('a').get('href')
                ret.append(url)

                findpdf = rst.findAll(attrs={'class': 'gs_ggs'})
                if findpdf:
                    pdflink = findpdf[0].find('a').get('href')
                    url = pdflink
                    ret.append(DirectPDFResource(url))
            except Exception as e:
                print color_text("Item parse error: {0}".format(str(e)), 'red')
                print traceback.format_exc()
        return ret

class GoogleSearcher(Searcher):
    GOOGLE_URL = "http://www.google.com.hk/search?q={0}"

    def __init__(self):
        self.name = "Google"

    def search(self, query):
        ret = []

        r = requests.get(GoogleSearcher.GOOGLE_URL.format(query))
        text = r.text.encode('utf-8')

        soup = BeautifulSoup(text)
        results = soup.findAll(attrs={'class': 'g'})
        for rst in results:
            try:
                h3 = rst.findAll('h3')[0]
                real_title = h3.get_text()
                if not title_correct(query, real_title):
                    continue
                findpdf = rst.findAll(attrs={'class': 'mime'})
                if findpdf and findpdf[0].text == '[PDF]':
                    pdflink = rst.findAll('a')[0].get('href')
                    url = GoogleSearcher.parse_google_link(pdflink)
                    ret.append(DirectPDFResource(url))
                else:
                    url = rst.findAll('a')[0].get('href')
                    url = GoogleSearcher.parse_google_link(url)
                    ret.append(url)
                print color_text("Found item on google: {0} at {1}".format(real_title,
                                                                urlparse(url).netloc),
                                 'blue')
            except Exception as e:
                print color_text("Item parse error: {0}".format(str(e)),
                                 'red')
                print traceback.format_exc()

        return ret

    @staticmethod
    def parse_google_link(url):
        real = re.findall('http[^&]*&', url)[0]
        ret = urllib.unquote(real[:-1])
        return ret

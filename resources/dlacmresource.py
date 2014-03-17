#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: dlacmresource.py
# Date: Mon Mar 17 09:45:39 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from resource import Resource
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse

class DL_ACM_Resource(Resource):
    HOSTNAME = 'dl.acm.org'

    def do_download(self, filename):
        print "Analyzing {0}".format(self.url)

        text = requests.get(self.url).text.encode('utf-8')
        #with open("/tmp/b.html", 'w') as f:
            #f.write(text)
        #text = open("/tmp/b.html").read()

        soup = BeautifulSoup(text)
        pdf = soup.findAll(attrs={'name': 'FullTextPDF'})
        url = pdf[0].get('href')
        url = 'http://{0}/'.format(DL_ACM_Resource.HOSTNAME) + url
        print "dl.acm origin url: {0}".format(url)

        r = requests.get(url, allow_redirects=False)
        url = r.headers.get('location')
        if url.find('pdf') != -1:
            return url
        r = requests.get(url, allow_redirects=False)
        url = r.headers.get('location')
        if url.find('pdf') != -1:
            Resource.direct_download(url, filename)

    @staticmethod
    def can_handle(url):
        url = urlparse(url)
        return url.netloc == DL_ACM_Resource.HOSTNAME


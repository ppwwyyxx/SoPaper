#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: ieeeresource.py
# Date: Mon Mar 17 10:47:42 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from resource import Resource
import re
from bs4 import BeautifulSoup
import requests
from urlparse import urlparse

class IEEExploreResource(Resource):
    def do_download(self, filename):
        print "Analyzing {0}".format(self.url)

        number = re.findall('arnumber=[0-9]*', self.url)[0]
        number = re.findall('[0-9]+', number)[0]
        url2 = "http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={0}".format(number)
        text = requests.get(url2).text.encode('utf-8')
        #with open("/tmp/b.html", 'w') as f:
            #f.write(text)
        #text = open('/tmp/a.html').read()

        soup = BeautifulSoup(text)
        fr = soup.findAll('frame')[-1]
        pdflink = fr.get('src')
        Resource.direct_download(pdflink, filename)

    @staticmethod
    def can_handle(url):
        url = urlparse(url)
        return url.netloc == 'ieeexplore.ieee.org'


if __name__ == '__main__':
    IEEExploreResource("http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=6599053").do_download("/tmp/a.pdf")

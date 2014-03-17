#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: arxiv.py
# Date: Mon Mar 17 14:13:50 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from resource import Resource
import re
from urlparse import urlparse

class ArxivResource(Resource):
    def do_download(self, filename):
        print "Analyzing {0}".format(self.url)

        PATTERN = re.compile('arxiv\.org/[^/]*/(?P<id>.*)')
        match = PATTERN.search(self.url).groupdict()
        pid = match['id']
        pdflink = "http://arxiv.org/pdf/{0}.pdf".format(pid)
        Resource.direct_download(pdflink, filename)

    @staticmethod
    def can_handle(url):
        url = urlparse(url)
        return url.netloc == 'arxiv.org'


if __name__ == '__main__':
    ArxivResource("http://arxiv.org/abs/1312.6680").do_download("/tmp/a.pdf")

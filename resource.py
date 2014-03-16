#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: resource.py
# Date: Sun Mar 16 22:22:34 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys
import requests

from urlparse import urlparse
from bs4 import BeautifulSoup
import requests

from text import parse_file_size
from utils import check_filetype
import traceback

def check_pdf(fname):
    return check_filetype(fname, 'PDF document')

class Resource(object):
    def __init__(self):
        self.url = None

    def download(self, filename):
        """return True/False"""
        try:
            self.do_download(filename)
        except Exception as e:
            print "Download error: {0}".format(str(e))
            print traceback.format_exc()
            return False
        else:
            if check_pdf(filename):
                return True
            else:
                print "Format is not PDF!"
                return False

    def do_download(self, ofile):
        pass


class DirectPDFResource(Resource):
    def __init__(self, url):
        self.url = url

    def do_download(self, filename):
        print "Directly Download PDF to {0}...".format(filename)
        print "PDF Link is {0}".format(self.url)

        resp = requests.get(self.url, stream=True)
        total_length = resp.headers.get('content-length')
        with open(filename, 'w') as f:
            if total_length is None:
                f.write(resp.content)
            else:
                total_length = int(total_length)
                print "File size is {0}".format(parse_file_size(total_length))
                dl = 0
                for data in resp.iter_content():
                    dl += len(data)
                    f.write(data)

                    width = 50
                    done_len = int(width * dl / total_length)
                    sys.stdout.write("\r[{0}>{1}]".format('=' * done_len,
                                                          ' ' * (width - done_len)))
                    sys.stdout.flush()
                print

class DL_ACM_Resource(Resource):
    HOSTNAME = 'dl.acm.org'

    def __init__(self, url):
        self.url = url

    def do_download(self, filename):
        print "Downloading from {0}".format(self.url)

        text = requests.get(self.url).text.encode('utf-8')
        with open("/tmp/b.html", 'w') as f:
            f.write(text)
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
            print "dl.acm pdf url: {0}".format(url)

    @staticmethod
    def can_handle(url):
        url = urlparse(url)
        return url.netloc == DL_ACM_Resource.HOSTNAME



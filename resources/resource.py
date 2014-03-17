#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: resource.py
# Date: Mon Mar 17 14:25:02 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys

import requests
from urlparse import urlparse

import os
from utils import check_filetype
import settings
from text import parse_file_size
from collections import defaultdict
import traceback

def check_pdf(fname):
    return check_filetype(fname, 'PDF document')

class Resource(object):
    def __init__(self, url):
        self.url = url

    #class __metaclass__(type):
        #__inheritors__ = defaultdict(list)

        #def __new__(meta, name, bases, dct):
            #klass = type.__new__(meta, name, bases, dct)
            #for base in klass.mro()[1:-1]:
                #meta.__inheritors__[base].append(klass)
            #return klass

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

    @staticmethod
    def get_handlers():
        ret = Resource.__subclasses__()
        return ret

    @staticmethod
    def direct_download(url, filename, headers=None):
        print "Directly Download to {0}...".format(filename)
        print "URL is {0}".format(url)

        if headers is None:
            headers = {'Host': urlparse(url).netloc,
                       'User-Agent': settings.USER_AGENT
                      }


        if settings.download_method == 'wget':
            headers = ' '.join(['--header="{0}: {1}"'.format(k, v) for k, v
                                in headers.iteritems()])
            os.system('wget "{0}" -O "{1}" {2}'.format(url, filename, headers))
            return

        resp = requests.get(url, stream=True, headers=headers)
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


class DirectPDFResource(Resource):
    def do_download(self, filename):
        Resource.direct_download(self.url, filename)

    @staticmethod
    def can_handle(url):
        return False

if __name__ == '__main__':
    print Resource.get_handlers()

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: downloader.py
# Date: Sun Dec 28 12:35:31 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys
if __name__ == '__main__':
    sys.path.append('../')
from uklogger import *
from lib.textutil import parse_file_size
from lib.exc import RecoverableErr
import ukconfig

import urllib
import os
import tempfile
import requests
from urlparse import urlparse

class ProgressPrinter(object):
    def __init__(self):
        self.total = 0
        self.last_done_len = -1

    def finish(self, data):
        sys.stdout.write("\n")
        sys.stdout.flush()
        log_info("Download finished")

    def update(self, done):
        assert self.total != 0
        width = 50
        done_len = int(width * done / self.total)
        if done_len > self.last_done_len:
            sys.stdout.write("\r[{0}>{1}]".format('=' * done_len,
                                                  ' ' * (width - done_len)))
            sys.stdout.flush()
        self.last_done_len = done_len

    def set_total(self, size):
        """size: number of bytes"""
        log_info("File size is {0}".format(parse_file_size(size)))
        self.total = size

def wget_download(url, progress_updater, headers=None):
    log_info("Download with wget on {0} ...".format(url))

    headers = ' '.join(['--header="{0}: {1}"'.format(k, v) for k, v
                        in headers.iteritems()])
    tf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    tf.close()
    # set timeout and retry number
    cmd = 'wget "{0}" -O "{1}" {2} --timeout=5 -t 3'.format(url, tf.name, headers)
    print cmd
    os.system(cmd)
    data = open(tf.name).read()
    progress_updater.finish(data)
    os.remove(tf.name)
    return data

def direct_download(url, progress_updater, headers=None):
    """ direct download according to ctx
        return the data
    """
    log_info("Directly Download with URL {0} ...".format(url))

    if headers is None:
        headers = {'Host': urlparse(url).netloc,
                   'User-Agent': ukconfig.USER_AGENT,
                   'Connection': 'Keep-Alive'
                  }

    # for test and cmd tools only
    if ukconfig.download_method == 'wget':
        return wget_download(url, progress_updater, headers)

    resp = requests.get(url, stream=True, headers=headers)
    total_length = resp.headers.get('content-length')
    if total_length is None:
        data = resp.content
        progress_updater.finish(data)
        return data
    else:
        total_length = int(total_length)
        if total_length < ukconfig.FILE_SIZE_MINIMUM:
            raise RecoverableErr("File too small: " + parse_file_size(total_length))
        if total_length > ukconfig.FILE_SIZE_MAXIMUM:
            raise RecoverableErr("File too large: " + parse_file_size(total_length))
        progress_updater.set_total(total_length)
        dl = 0
        ret = ""
        for data in resp.iter_content():
            dl += len(data)
            ret += data
            progress_updater.update(dl)
        progress_updater.finish(data)
        return ret

if __name__ == '__main__':
    data = direct_download('http://delivery.acm.org/10.1145/330000/322274/p615-yao.pdf?ip=59.66.132.22&id=322274&acc=ACTIVE%20SERVICE&key=BF85BBA5741FDC6E%2E587F3204F5B62A59%2E4D4702B0C3E38B35%2E4D4702B0C3E38B35&CFID=456185443&CFTOKEN=45860210&__acm__=1399725544_eebbed2ce2719c67c7a3642f2b21d80a')
    print data

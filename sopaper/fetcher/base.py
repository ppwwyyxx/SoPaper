#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: base.py
# Date: Thu Jun 25 16:29:22 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from ..uklogger import *
from ..lib.downloader import direct_download, ProgressPrinter
from ..lib.exc import RecoverableErr
from ..lib.textutil import title_beautify

class FetcherBase(object):

    def __init__(self, search_result):
        self.search_result = search_result
        self.url = self.search_result.url
        self.title = None
        self.meta = None
        self.name = None
        self.data = None

        self.headers = None
        try:
            self._do_pre_parse()
        except Exception as e:
            log_exc("Exception in pre-parse")

    def _do_pre_parse(self):
        """ parse right after getting the url"""

    def _do_download(self, updater):
        """ return data, or raise"""

    def _do_get_meta(self):
        """ return dict"""
        pass

    def _do_get_title(self):
        """ return string, or raise"""
        pass

    def get_meta(self):
        if self.meta is not None:
            return self.meta
        self.meta = self._do_get_meta()
        return self.meta

    def get_title(self):
        if self.title is not None:
            if not self.title:
                return None
            else:
                return self.title
        try:
            self.title = title_beautify(self._do_get_title())
            return self.title
        except:
            self.title = ""
            return None

    def download(self, updater=None):
        """ save self.data"""
        if updater is None:
            updater = ProgressPrinter()
        try:
            self.data = self._do_download(updater)
            return True
        except KeyboardInterrupt:
            raise
        except RecoverableErr as e:
            log_err(str(e))
            return False
        except Exception:
            log_exc("Error while downloading with" \
                    "url '{0}'".format(self.url))
            return False

    def get_data(self):
        if self.data is None:
            raise Exception("Cannot call get_data() before download succeeds")
        return self.data

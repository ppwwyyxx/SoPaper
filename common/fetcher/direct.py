#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: direct.py
# Date: Sat May 24 16:00:45 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
from .base import FetcherBase, direct_download

@register_parser(name='direct link', urlmatch='.*\.pdf', typematch='directpdf')
class DirectPdf(FetcherBase):
    def _do_download(self, updater):
        return direct_download(self.url, updater)

    def _do_get_title(self):
       raise Exception("Cannot get title from direct pdf link" )

    def _do_get_meta(self):
       return {}

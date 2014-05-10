#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: arxiv.py
# Date: Sat May 10 19:16:07 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser
import re

ARXIV_PAT = re.compile('arxiv\.org/[^/]*/(?P<id>.*)')

@register_parser(name='arxiv.org', urlmatch='arxiv.org')
def arxiv(search_result):
    url = search_result.url
    match = ARXIV_PAT.search(url).groupdict()
    pid = match['id']
    pdflink = "http://arxiv.org/pdf/{0}.pdf".format(pid)
    return {'url': pdflink }

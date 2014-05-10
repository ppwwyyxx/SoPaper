#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: ieee.py
# Date: Sat May 10 19:29:43 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from . import register_parser

import re
from bs4 import BeautifulSoup
import requests

@register_parser(name='ieeexplore.ieee.org',urlmatch='ieeexplore.ieee.org')
def ieee(search_result):
    url = search_result.url

    number = re.findall('arnumber=[0-9]*', url)[0]
    number = re.findall('[0-9]+', number)[0]
    url2 = "http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={0}".format(number)
    text = requests.get(url2).text.encode('utf-8')

    #with open("/tmp/b.html", 'w') as f:
        #f.write(text)
    #text = open('/tmp/a.html').read()

    soup = BeautifulSoup(text)
    fr = soup.findAll('frame')[-1]
    pdflink = fr.get('src')
    return {'url': pdflink}

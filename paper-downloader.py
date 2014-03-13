#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Thu Mar 13 14:48:46 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import argparse
import operator
import string
from urlparse import urlparse
import os
import sys
import os.path
import requests
from bs4 import BeautifulSoup

import handlers
from text import levenshtein, title_beautify, parse_file_size

GOOGLE_SCHOLAR_URL = "http://scholar.google.com/scholar?hl=en&q={0}&btnG=&as_sdt=1%2C5&as_sdtp="

HANDLERS = [handlers.dl_acm_org]


def judge(query, title):
    q = ''.join([t for t in query if t in string.letters])
    now = ''.join([t for t in title if t in string.letters]).lower()
    return levenshtein(q, now) < 7

def get_args():
    desc = 'Automatic Search and download paper'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('-t', '--title',
                        help='Title of the paper', required=True)
    parser.add_argument('-d', '--directory',
                        help='Output Directory (default: current directory)',
                        required=False, default='.')

    ret = parser.parse_args()
    return ret

def parse_side_link(link):
    # parse arxiv
    return link

def parse_title_link(link):
    parsed = urlparse(link)
    for h in HANDLERS:
        test = h(parsed)
        if test:
            print "Get download link {0} from page {1}".format(test, link)
            return test
    return None

def download(title, pdflink):
    title = title_beautify(title)
    print "Get paper: {0}".format(title)

    ofile = os.path.join(args.directory, title + '.pdf')

    print "Downloading to {0}...".format(ofile)
    print "PDF Link is {0}".format(pdflink)

    with open(ofile, 'w') as f:
        resp = requests.get(pdflink, stream=True)
        total_length = resp.headers.get('content-length')
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
    print "Download finished."


def parse_scholar(query):
    print "Searching on Google Scholar..."
    query = query.lower()
    #r = requests.get(GOOGLE_SCHOLAR_URL.format(query))
    #text = r.text.encode('utf-8')
    #with open("/tmp/a.html", 'w') as f:
        #f.write(text)
    text = open("/tmp/a.html", 'r').read()
    soup = BeautifulSoup(text)
    results = soup.findAll(attrs={'class': 'gs_r'})
    for rst in results:
        h3 = rst.findAll('h3')[0]
        real_title = h3.get_text()
        if not judge(query, real_title):
            continue
        findpdf = rst.findAll(attrs={'class': 'gs_ggs'})
        if not findpdf:
            url = h3.find('a').get('href')
            url = parse_title_link(url)
            if not url:
                continue
        else:
            pdflink = findpdf[0].find('a').get('href')
            pdflink = parse_side_link(pdflink)
            download(real_title, pdflink)
    return False

def main():
    global args
    args = get_args()

    parse_scholar(args.title)


if __name__ == '__main__':
    main()

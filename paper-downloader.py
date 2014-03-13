#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Thu Mar 13 12:29:56 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import argparse
import operator
import os
import sys
import os.path
import requests
from bs4 import BeautifulSoup

GOOGLE_SCHOLAR_URL = "http://scholar.google.com/scholar?hl=en&q={0}&btnG=&as_sdt=1%2C5&as_sdtp="

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

def parse_real_link(link):
    # parse arxiv
    return link

def title_beautify(title):
    return title

def parse_file_size(size):
    if size > 1000000:
        return "{0:.2f}MB".format(float(size) / 1000000)
    if size > 1000:
        return "{0:.2f}KB".format(float(size) / 1000)
    return "{0}B".format(size)

def download(title, pdflink):
    title = title_beautify(title)
    print "Get paper: {0}".format(title)

    ofile = os.path.join(args.directory, title + '.pdf')
    pdflink = parse_real_link(pdflink)

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
    token_set = set(query.split())
    r = requests.get(GOOGLE_SCHOLAR_URL.format(query))
    print r.text.encode('utf-8')
    text = open('/tmp/a.html').read()
    soup = BeautifulSoup(text)
    results = soup.findAll(attrs={'class': 'gs_r'})
    candidates = []
    for rst in results:
        real_title = rst.findAll('h3')[0].get_text()
        now_token_set = set(real_title.lower().split())
        simi = len(token_set & now_token_set)

        findpdf = rst.findAll(attrs={'class': 'gs_ggs'})
        if not findpdf:
            continue
        pdflink = findpdf[0].find('a').get('href')
        candidates.append((real_title, simi, pdflink))
    candidates = sorted(candidates, key=operator.itemgetter(1), reverse=True)
    if candidates[0][1] > 4:
        t = candidates[0]
        download(t[0], t[2])


def main():
    global args
    args = get_args()

    parse_scholar(args.title)


if __name__ == '__main__':
    main()

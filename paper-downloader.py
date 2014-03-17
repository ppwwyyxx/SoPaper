#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Mon Mar 17 10:19:43 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import argparse
import os
import sys
import os.path

from text import title_beautify
from searcher import ScholarSearcher, GoogleSearcher
from resources.resource import Resource
import resources


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

def main():
    global args
    args = get_args()

    title = title_beautify(args.title)

    ofile = os.path.join(args.directory, args.title + '.pdf')

    query = args.title.lower()
    searchers = [ScholarSearcher(), GoogleSearcher()]
    #searchers = [GoogleSearcher()]
    for s in searchers:
        resources = s.search(query)
        print resources
        for r in resources:
            if isinstance(r, basestring):
                for h in Resource.get_handlers():
                    if h.can_handle(r):
                        if h(r).download(ofile):
                            return
            else:
                if r.download(ofile):
                    return


if __name__ == '__main__':
    main()

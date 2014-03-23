#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Mon Mar 24 00:17:07 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import argparse
import os
import sys
import os.path

from text import title_beautify, color_text
from searcher import ScholarSearcher, GoogleSearcher
import settings
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

def get_ofile_name():
    return os.path.join(args.directory, title_beautify(settings.title) + '.pdf')

def main():
    global args
    args = get_args()

    settings.title = args.title
    #title = title_beautify(args.title)

    #settings.ofile = os.path.join(args.directory, title + '.pdf')

    query = args.title.lower()
    searchers = [ScholarSearcher(), GoogleSearcher()]
    #searchers = [GoogleSearcher()]
    for s in searchers:
        print color_text("Searching with {0}".format(s.name), 'green')
        rsts = s.search(query)
        for r in rsts:
            if isinstance(r, basestring):
                for h in Resource.get_handlers():
                    if h.can_handle(r):
                        if h(r).download(get_ofile_name()):
                            return
            else:
                if r.download(get_ofile_name()):
                    return


if __name__ == '__main__':
    main()

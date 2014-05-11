#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Sun May 11 13:36:21 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

# Command line script to use paper-downloader
# You don't need to setup virtualenv to use script
# But you'll need requests and BeautifulSoup4 installed

import sys
import os
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'common'))

import searcher
from job import JobContext
import fetcher

import argparse

def get_args():
    desc = 'SoPaper command line tool -- ' \
        'Fully Automated Paper Searcher & Downloader' \
        '\nSoPaper, So Easy'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('-t', '--title',
                        help='Title of the paper', required=True)
    parser.add_argument('-d', '--directory',
                        help='Output Directory (default: current directory)',
                        required=False, default='.')
    ret = parser.parse_args()
    return ret

def main():
    global args
    args = get_args()

    query = args.title
    directory = args.directory
    #query = "Distinctive image features from scale-invariant keypoint"
    ctx = JobContext(query)

    searcher_lst = searcher.register_searcher.get_searcher_list()
    parser_lst = fetcher.register_parser.get_parser_list()

    for s in searcher_lst:
        res = s.run(ctx)
        for sr in res:
            for parser in parser_lst:
                succ = parser.run(ctx, sr)
                if succ:
                    filename = os.path.join(directory, ctx.title + ".pdf")
                    log_info("Writing data to {0}".format(filename))
                    try:
                        with open(filename, 'wb') as f:
                            f.write(ctx.data)
                    except IOError:
                        log_exc("Failed to write to file")
                    return


if __name__ == '__main__':
    main()

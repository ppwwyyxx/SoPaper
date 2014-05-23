#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Fri May 23 21:06:18 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

# Command line script to use paper-downloader
# You don't need to setup virtualenv to use script
# But you'll need requests and BeautifulSoup4 installed

import sys
import os
import os.path
from multiprocessing import Pool
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

    searchers = searcher.register_searcher.get_searcher_list()
    parsers = fetcher.register_parser.get_parser_list()

    args = zip(searchers, [ctx] * len(searchers))
    pool = Pool()
    as_results = [pool.apply_async(search_run, arg) for arg in args]

    for s in as_results:
        s = s.get()
        srs = s['results']
        for sr in srs:
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

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Mon May 26 20:01:38 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

# Command line script to use paper-downloader
# You don't need to setup virtualenv to use script
# But you'll need requests and BeautifulSoup4 installed

import sys
import os
import os.path
import argparse
from multiprocessing import Pool
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'common'))

import searcher
from searcher import searcher_run
from job import JobContext
import fetcher
from fetcher import do_fetcher_download
from ukutil import pdf_compress
from uklogger import *
import ukconfig
ukconfig.download_method = 'wget'

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
    download_candidates = []

    for s in as_results:
        s = s.get()
        if s is None:
            continue
        srs = s['results']

        # try search database with updated title
        try:
            updated_title = s['ctx_update']['title']
        except KeyError:
            pass
        else:
            if updated_title != ctx.title:
                log_info("Using new title: {0}".format(updated_title))
                ctx.title = updated_title

        for sr in srs:
            for parser in parsers:
                if parser.can_handle(sr):
                    download_candidates.append((parser, sr))

    for (parser, sr) in download_candidates:
        data = parser.download(sr)
        if data:
            try:
                data = pdf_compress(data)
            except:
                log_err("PDF compress failed, you may need to install poppler-utils")
            filename = os.path.join(directory, ctx.title + ".pdf")
            log_info("Writing data to {0}".format(filename))
            try:
                with open(filename, 'wb') as f:
                    f.write(data)
            except IOError:
                log_exc("Failed to write to file")
            return


if __name__ == '__main__':
    main()

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

# Command line script to use paper-downloader
# You don't need to setup virtualenv to use script
# But you'll need requests and BeautifulSoup4 installed

import sys
import os
import re
import os.path
import argparse
from multiprocessing import Pool
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'common'))

# Config must be set at the beginning
import ukconfig
ukconfig.download_method = 'wget'
ukconfig.USE_DB = False
ukconfig.LOG_DIR = None

import searcher
from searcher import searcher_run
from job import JobContext, SearchResult
import fetcher
from lib.pdfutil import pdf_compress
from lib.textutil import norm_filename, md5
from uklogger import *

def get_args():
    desc = 'SoPaper command line tool -- ' \
        'Fully Automated Paper Searcher & Downloader' \
        '\nSoPaper, So Easy'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('title', help='Title of the paper or URL of an arxiv/ieee/dlacm page')
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


    searchers = searcher.register_searcher.get_searcher_list()
    parsers = fetcher.register_parser.get_parser_list()
    download_candidates = []
    if re.match('^http[s]?://', query):
        # skip search
        ctx = JobContext("")
        sr = SearchResult(None, query)
        for parser in parsers:
            if parser.can_handle(sr):
                parser.fetch_info(ctx, sr)      # will update title
                download_candidates.append((parser, sr))
    else:
        #query = "Distinctive image features from scale-invariant keypoint"
        ctx = JobContext(query)

        args = zip(searchers, [ctx] * len(searchers))
        pool = Pool()
        as_results = [pool.apply_async(searcher_run, arg) for arg in args]

        for s in as_results:
            s = s.get()
            if s is None:
                continue
            ctx.update_meta_dict(s['ctx_update'])
            print s['ctx_update']
            ctx.try_update_title_from_search_result(s)

            for sr in s['results']:
                for parser in parsers:
                    if parser.can_handle(sr):
                        parser.fetch_info(ctx, sr)      # will update title
                        download_candidates.append((parser, sr))
        pool.terminate()

    download_candidates = sorted(
        download_candidates,
        key=lambda x: x[0].priority,
        reverse=True)

    for (parser, sr) in download_candidates:
        data = parser.download(sr)
        if data:
            data = pdf_compress(data)
            if ctx.title:
                ctx.title = norm_filename(ctx.title)
            else:
                log_info("No known paper title!")
                ctx.title = "Unnamed Paper {}".format(md5(data))

            filename = os.path.join(directory, ctx.title + ".pdf")
            if os.path.exists(filename):
                log_err("File {} exists! exit".format(os.path.basename(filename)))
                break
            with open(filename, 'wb') as f:
                f.write(data)
            log_info("Successfully downloaded to {0}".format(filename))
            break
    else:
        log_err("Failed to download {0}".format(ctx.title))
    if ctx.meta.get('bibtex'):
        log_info("Bibtex:\n{}".format(ctx.meta['bibtex']))
    if ctx.meta.get('author'):
        log_info("Author: {0}".format(ctx.meta['author']))
    if ctx.meta.get('citecnt'):
        log_info("Cite count: {0}".format(ctx.meta['citecnt']))

if __name__ == '__main__':
    main()

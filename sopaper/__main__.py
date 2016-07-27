#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: __main__.py
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

# Config must be set at the beginning
from sopaper import ukconfig
ukconfig.download_method = 'wget'
ukconfig.USE_DB = False
ukconfig.LOG_DIR = None

from sopaper import searcher
from sopaper.searcher import searcher_run
from sopaper.job import JobContext, SearchResult
from sopaper import fetcher
from sopaper.lib.pdfutil import pdf_compress
from sopaper.lib.textutil import finalize_filename, md5
from sopaper.uklogger import *

def get_args():
    desc = 'SoPaper command line tool -- ' \
        'Fully Automated Paper Searcher & Downloader' \
        '\nSoPaper, So Easy'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('title', nargs='+', help='Title of the paper or URL of an arxiv/ieee/dlacm page')
    parser.add_argument('-u', '--url', action='store_true', help='do not download, print URL only')
    parser.add_argument('-d', '--directory',
                        help='Output Directory (default: current directory)',
                        required=False, default='.')
    parser.add_argument('-o', '--output',
                        help='Manually specify a output file, rather than automatically determine the correct name.')
    ret = parser.parse_args()
    ret.title = ' '.join(ret.title)
    return ret

def main():
    global args
    args = get_args()
    query = args.title.strip()
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

        search_args = zip(searchers, [ctx] * len(searchers))
        pool = Pool()
        as_results = [pool.apply_async(searcher_run, arg) for arg in search_args]
        #results = [searcher_run(*arg) for arg in search_args]  # for debug

        url_seen = set()    # avoid repeated url
        for s in as_results:
            s = s.get(ukconfig.PYTHON_POOL_TIMEOUT)
            if s is None:
                continue
            ctx.update_meta_dict(s['ctx_update'])
            ctx.try_update_title_from_search_result(s)

            for sr in s['results']:
                if sr.url in url_seen:
                    continue
                url_seen.add(sr.url)
                for parser in parsers:
                    if parser.can_handle(sr):
                        parser.fetch_info(ctx, sr)      # will update title
                        download_candidates.append((parser, sr))
        pool.terminate()

    download_candidates = sorted(
        download_candidates,
        key=lambda x: x[0].priority,
        reverse=True)

    if ctx.title:
        ctx.title = finalize_filename(ctx.title)
    else:
        log_info("Failed to guess paper title!")
        ctx.title = "Unnamed Paper"
    if args.url:
        # url mode
        print("Results for {}:".format(ctx.title))
        for (_, sr) in download_candidates:
            print(sr.url)
        return

    for (parser, sr) in download_candidates:
        data = parser.download(sr)
        if not data:
            continue
        data = pdf_compress(data)

        filename = os.path.join(directory, ctx.title + ".pdf")
        if os.path.exists(filename):
            log_err("File \"{}\" exists! overwrite? (y/n)".format(os.path.basename(filename)))
            resp = raw_input()
            if resp not in ['y', 'Y']:
                log_info("No file written. Exiting...")
                break
        with open(filename, 'wb') as f:
            f.write(data)
        if args.output:
            os.rename(filename, args.output)
        break
    else:
        log_err("Failed to download {0}".format(ctx.title))
        return
    if ctx.meta.get('bibtex'):
        log_info("Bibtex:\n{}".format(ctx.meta['bibtex']))
    if ctx.meta.get('author'):
        log_info("Author: {0}".format(ctx.meta['author']))
    if ctx.meta.get('citecnt'):
        log_info("Cite count: {0}".format(ctx.meta['citecnt']))
    log_info("Successfully downloaded to {0}".format(filename))

if __name__ == '__main__':
    main()

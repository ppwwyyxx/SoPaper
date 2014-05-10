#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: paper-downloader.py
# Date: Sat May 10 17:15:57 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import searcher
from job import JobContext
import fetcher


def main():
    query = "Distinctive image features from scale-invariant keypoints"

    searcher_lst = searcher.register_searcher.searcher_list
    parser_lst = fetcher.register_parser.parser_list
    ctx = JobContext(query)
    for s in searcher_lst:
        res = s.run(ctx)
        print [str(r) for r in res]
        for sr in res:
            for parser in parser_lst:
                suc = parser.run(ctx, sr)
                if suc:
                    return


if __name__ == '__main__':
    main()

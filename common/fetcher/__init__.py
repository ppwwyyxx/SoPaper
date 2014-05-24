#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: __init__.py
# Date: Sat May 24 16:01:03 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from lib.downloader import direct_download, ProgressPrinter
from lib.textutil import title_beautify
from ukutil import check_pdf, import_all_modules
from uklogger import *
from job import SearchResult
from dbsearch import search_exact
from lib.exc import RecoverableErr

try:
    import ukdbconn
except ImportError:
    pass

from functools import wraps
import ukconfig
import re

class register_parser(object):
    parser_dict = {}
    """ save the original parser func"""

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        self.url_match = re.compile(kwargs.pop('urlmatch'))

        self.type_match = kwargs.pop('typematch', None)
        self.legal = kwargs.pop('legal', True)

        assert self.name not in self.parser_dict

    @staticmethod
    def get_parser_list():
        return register_parser.parser_dict.values()

    def __call__(self, fetcher_cls):
        """ fetcher_cls: subclass of FetcherBase to be used
            'url', 'headers' to pass to downloader,
            'ctx_update': a dict to update the context
        """

        @wraps(fetcher_cls)
        def wrapper(res):
            assert isinstance(res, SearchResult)
            try:
                fetcher = fetcher_cls(res)
                fetcher.name = self.name
                fetcher.get_title()
                fetcher.get_meta()
                return fetcher
            except KeyboardInterrupt:
                raise
            except Exception:
                log_exc("Error in parser '{0}' with url '{1}'".
                        format(self.name, res.url))
                return None
        self.parser_dict[self.name] = self
        self.cb = wrapper
        return wrapper

    def run(self, ctx, sr, progress_updater=None):
        """ run this parser against the SearchResult given
            return True/False indicate success,
            will update ctx metadata and ctx.success,

            on success, either ctx will be filled with fetched data,
                        or ctx.existing will contain a existing doc in db.
        """
        url = sr.url
        if (self.type_match is None
            or self.type_match != sr.type) and \
           len(self.url_match.findall(url)) == 0:
            return False

        log_info("Parsing url {0} with parser {1}".
                 format(url, self.name))
        fetcher_inst = self.cb(sr)
        if fetcher_inst is None:
            return False

        # check updated title against db before download
        newt = fetcher_inst.get_title()
        if newt and newt != ctx.title:
            ctx.title = newt
            log_info("Using new title: {0}".format(ctx.title))
            if ukconfig.USE_DB:
                doc = search_exact(newt)
                if res:
                    ctx.existing = doc
                    ukdbconn.update_meta(doc['_id'], fetcher_inst.get_meta())
                    return True
        log_info("Update metadata: {0}".format(str(fetcher_inst.get_meta().keys())))
        ctx.update_meta_dict(fetcher_inst.get_meta())

        if progress_updater is None:
            progress_updater = ProgressPrinter()
        succ = fetcher_inst.download(progress_updater)
        if not succ:
            return False

        ft = check_pdf(fetcher_inst.get_data())
        #ft = True
        if ft == True:
            ctx.success = True
            ctx.data = fetcher_inst.get_data()
            return True
        else:
            log_err("Wrong Format: {0}".format(ft))
            return False



if __name__ != '__main__':
    import_all_modules(__file__, __name__)


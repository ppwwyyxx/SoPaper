#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: __init__.py
# Date: Tue Jun 10 22:44:13 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from lib.downloader import direct_download, ProgressPrinter
from lib.textutil import title_beautify
from lib.ukutil import check_pdf, import_all_modules, ensure_unicode
from uklogger import *
from job import SearchResult
from lib.exc import RecoverableErr

try:
    import ukdbconn
    from dbsearch import search_exact
except ImportError:
    # for cmd tools to use
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

        """ priority of this parser, higher for those unlikely to be blocked"""
        self.priority = kwargs.pop('priority', 5)

        self.type_match = kwargs.pop('typematch', None)
        self.legal = kwargs.pop('legal', True)

        """ what meta field this fetcher might provide"""
        self.support_meta_field = kwargs.pop('meta_field', [])

        """ whether this fetcher should be considered multiple times l
            during a search.
            For now, only 'DirectPdfParser' shall be considered multiple times
        """
        self.repeatable = kwargs.pop('repeatable', False)

        assert self.name not in self.parser_dict

    @staticmethod
    def get_parser_list():
        lst = register_parser.parser_dict.values()
        return sorted(lst, key=lambda x: x.priority, reverse=True)

    def __call__(self, fetcher_cls):
        """ fetcher_cls: subclass of FetcherBase to be used
        """
        self.fetcher_cls = fetcher_cls

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

    def can_handle(self, sr):
        if (self.type_match is None
            or self.type_match != sr.type) and \
           len(self.url_match.findall(sr.url)) == 0:
            return False
        return True

    def fetch_info(self, ctx, sr):
        """ run this parser against the SearchResult given
            return True/False indicate success,
            will update ctx metadata and ctx.success,

            on success, either ctx will be filled with fetched data,
                        or ctx.existing will contain a existing doc in db.
        """
        url = sr.url
        log_info("Parsing url {0} with parser {1}".
                 format(url, self.name))
        fetcher_inst = self.cb(sr)
        if fetcher_inst is None:
            return False

        newt = fetcher_inst.get_title()
        if newt and newt != ctx.title:
            ctx.title = newt
            log_info(u"Using new title: {0}".format(ensure_unicode(ctx.title)))

            # check updated title against db before download
            if ukconfig.USE_DB:
                doc = search_exact(newt)
                if doc:
                    ctx.existing = doc[0]
                    ukdbconn.update_meta(doc[0]['_id'], fetcher_inst.get_meta())
                    return True
        log_info("Fetcher Update Metadata: {0}".format(str(fetcher_inst.get_meta().keys())))
        ctx.update_meta_dict(fetcher_inst.get_meta())
        # if can download
        ctx.add_downloader(fetcher_inst)
        return True

    def download(self, sr, progress_updater=None):
        fetcher_inst = self.fetcher_cls(sr)

        succ = fetcher_inst.download(progress_updater)
        if not succ:
            return None

        ft = check_pdf(fetcher_inst.get_data())
        if ft == True:
            data = fetcher_inst.get_data()
            return data
        else:
            log_err("Wrong Format: {0}".format(ft))
            return None


if __name__ != '__main__':
    import_all_modules(__file__, __name__)


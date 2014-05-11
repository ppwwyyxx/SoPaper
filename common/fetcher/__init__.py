#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: __init__.py
# Date: Sun May 11 13:20:24 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from lib.downloader import direct_download, ProgressPrinter
from ukutil import check_pdf, import_all_modules
from uklogger import *
from job import SearchResult

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
        self.custom_downloader = kwargs.pop('custom_downloader', None)

        assert self.name not in self.parser_dict

    @staticmethod
    def get_parser_list():
        return register_parser.parser_dict.values()

    def __call__(self, func):
        """ func: callable to be invoked, took a 'SearchResult'
            func return a dict, with
            'url', 'headers' to pass to downloader,
            'ctx_update': {} to update the context
        """

        @wraps(func)
        def wrapper(res):
            assert isinstance(res, SearchResult)
            try:
                params = func(res)
                if params is None:
                    return None
                if 'ctx_update' not in params:
                    params['ctx_update'] = {}
                params['ctx_update'].update({
                    'source': self.name,
                    'page_url': res.url
                })
                if params['ctx_update'].get('title'):
                    params['ctx_update']['title'] = title_beautify(params['ctx_update']['title'])
                return params
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
        res = self.cb(sr)
        if res is None:
            return False

        # check updated title against db before download
        if ukconfig.USE_DB:
            newt = res['ctx_update'].get('title')
            if  newt != ctx.title:
                doc = search_exact(newt)
                if res:
                    ctx.existing = doc
                    ukdbconn.update_meta(doc['_id'], res['ctx_update'])
                    return True

        try:
            if progress_updater is None:
                progress_updater = ProgressPrinter()
            if self.custom_downloader is None:
                data = direct_download(res['url'], progress_updater,
                                       res.get('headers'))
            else:
                data = self.custom_downloader(res, progress_updater)
        except KeyboardInterrupt:
            raise
        except Exception:
            log_exc("Error while downloading in parser '{0}' with" \
                    "url '{1}'".format(self.name, url))
            return False

        ft = check_pdf(data)
        if ft == True:
            ctx.success = True
            ctx.data = data
            log_info("Update metadata: {0}".format(str(res['ctx_update'])))
            ctx.update_meta_dict(res['ctx_update'])
            return True
        else:
            log_err("Wrong Format: {0}".format(ft))
            return False


@register_parser(name='direct link', urlmatch='.*\.pdf', typematch='directpdf')
def direct_link(search_result):
    return { 'url': search_result.url}

if __name__ != '__main__':
    import_all_modules(__file__, __name__)


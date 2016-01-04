#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: __init__.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from functools import wraps

from ..lib.ukutil import import_all_modules
from ..uklogger import *
from ..job import JobContext

def searcher_run(searcher, ctx):
    """ a global function to invoke with multiprocessing,
        run a searcher against a JobContext"""
    return searcher.run(ctx)

class register_searcher(object):
    searcher_list = []

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        self.priority = kwargs.pop('priority', 5)

    def __call__(self, func):
        """ func: callable to be invoked, took a JobContext
            func cannot change JobContext
            func return a dict with keys:
                results : list of 'SearchResult'
                ctx_update: dict
        """

        @wraps(func)
        def wrapper(ctx):
            assert isinstance(ctx, JobContext)
            try:
                log_info("Searching '{1}' with searcher: '{0}' ...".
                         format(self.name, ctx.query))
                res = func(ctx)
                for r in res['results']:
                    r.searcher = self.name
                return res
            except KeyboardInterrupt:
                raise
            except Exception as e:
                log_exc("Error in searcher '{0}' with query '{1}': {2}".
                        format(self.name, ctx.query, str(e)))

        self.searcher_list.append(self)
        self.cb = wrapper
        return wrapper

    def run(self, ctx):
        """ run this searcher against the context given"""
        res = self.cb(ctx)
        if res and res['results']:
            log_info("Got the following results from {0}:\n".format(self.name) +
                    "\n".join([str(r) for r in res['results']]))
        return res

    @staticmethod
    def get_searcher_list():
        return sorted(register_searcher.searcher_list, key=lambda x: x.priority, reverse=True)

import_all_modules(__file__, __name__)

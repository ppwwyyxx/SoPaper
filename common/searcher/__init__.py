#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: __init__.py
# Date: Sat May 10 17:57:24 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from ukutil import import_all_modules
from uklogger import *
from functools import wraps

from job import JobContext

class register_searcher(object):
    searcher_list = []

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        self.priority = kwargs.pop('priority', 5)

    def __call__(self, func):
        """ func: callable to be invoked, took a JobContext
            func return list of 'SearchResult'
        """

        @wraps(func)
        def wrapper(ctx):
            assert isinstance(ctx, JobContext)
            try:
                log_info("Searching '{1}' with searcher: '{0}' ...".
                         format(self.name, ctx.query))
                res = func(ctx)
                for r in res:
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
        if res:
            ctx.search_results.extend(res)
            log_info("Got the following results from {0}:\n".format(self.name) +
                    "\n".join([str(r) for r in res]))
        return res

    @staticmethod
    def get_searcher_list():
        return sorted(register_searcher.searcher_list, key=lambda x: x.priority, reverse=True)

import_all_modules(__file__, __name__)

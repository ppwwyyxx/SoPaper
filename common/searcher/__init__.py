#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: __init__.py
# Date: Sat May 10 17:09:00 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from ukutil import import_all_modules
from uklogger import *
from functools import wraps

from job import JobContext

class register_searcher(object):
    searcher_list = []

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')

    def __call__(self, func):
        """ func: callable to be invoked, took a JobContext
            func return list of 'SearchResult'
        """

        @wraps(func)
        def wrapper(ctx):
            assert isinstance(ctx, JobContext)
            try:
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
        return res

import_all_modules(__file__, __name__)

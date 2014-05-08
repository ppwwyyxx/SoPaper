#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: singleton.py
# Date: Sat Mar 29 16:28:50 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

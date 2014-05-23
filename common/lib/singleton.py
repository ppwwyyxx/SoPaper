#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: singleton.py
# Date: Fri May 23 22:12:27 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls,*args,**kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

def dec_singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

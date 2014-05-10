#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukutil.py
# $Date: Sat May 10 17:26:31 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""common utility functions"""

from importlib import import_module
from pkgutil import walk_packages
from datetime import datetime
from subprocess import Popen, PIPE
import os

def ensure_unicode(s):
    """assert type of s is basestring and convert s to unicode"""
    assert isinstance(s, basestring), 's should be string'
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s

def ensure_bin_str(s):
    """assert type of s is basestring and convert s to byte string"""
    assert isinstance(s, basestring), 's should be string'
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    return s

def import_all_modules(file_path, pkg_name):
    """import all modules recursively in a package
    :param file_path: just pass __file__
    :param pkg_name: just pass __name__
    """
    for _, module_name, _ in walk_packages(
            [os.path.dirname(file_path)], pkg_name + '.'):
        import_module(module_name)

def check_filetype(f, need_type):
    s = Popen('file "{0}"'.format(f), stdout=PIPE, shell=True).stdout.read()
    if s.find(need_type) != -1:
        return True
    else:
        print s
        return False

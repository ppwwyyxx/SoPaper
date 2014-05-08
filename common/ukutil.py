#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: ukutil.py
# $Date: Tue Apr 22 19:17:44 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""common utility functions"""

from importlib import import_module
from pkgutil import walk_packages
from datetime import datetime
import re
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

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def name_clean(name):
    p = re.compile('\(.*?\)', re.DOTALL)
    ret = p.sub('', name).strip()
    return ensure_unicode(ret)

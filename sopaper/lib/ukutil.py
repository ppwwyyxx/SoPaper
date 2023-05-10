#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: ukutil.py
# Date: Fri Jun 02 10:18:29 2017 -0700
# Author: jiakai <jia.kai66@gmail.com>
#         Yuxin Wu <ppwwyyxxc@gmail.com>

"""common utility functions"""
from importlib import import_module
from pkgutil import walk_packages
from datetime import datetime
from subprocess import Popen, PIPE
import tempfile
import os

from .. import ukconfig
from ..uklogger import *


try:
    import magic
except:
    pass

def ensure_unicode_anytype(s):
    if isinstance(s, str):
        return ensure_unicode(s)
    return s

def ensure_unicode(s):
    """assert type of s is basestring and convert s to unicode"""
    assert isinstance(s, str), 's should be string' + str(s)
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s

def ensure_bin_str(s):
    """assert type of s is basestring and convert s to byte string"""
    assert isinstance(s, str), 's should be string'
    if isinstance(s, str):
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

def check_buf_filetype(buf, need_type):
    if ukconfig.USE_MAGIC_LIB:
        s = magic.from_buffer(buf)
    else:
        assert os.name != 'nt', "Windows users please install python-magic."
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(buf)
        f.close()
        s = Popen('file "{0}"'.format(f.name),
                  stdout=PIPE, shell=True).stdout.read()
        os.unlink(f.name)
    if s.find(need_type) != -1:
        return True
    else:
        return False

def check_file_type(fname, need_type):
    s = Popen('file "{0}"'.format(fname), stdout=PIPE, shell=True).stdout.read()
    if s.find(need_type) != -1:
        return True
    return False


if __name__ == '__main__':
    print(check_filetype(open("./ukconfig.py").read(), 'PDF'))

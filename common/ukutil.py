#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File: ukutil.py
# Date: 一 6月 09 16:47:48 2014 +0000
# Author: jiakai <jia.kai66@gmail.com>
#         Yuxin Wu <ppwwyyxxc@gmail.com>

"""common utility functions"""

import ukconfig
from uklogger import *
from importlib import import_module
from pkgutil import walk_packages
from datetime import datetime
from subprocess import Popen, PIPE
from lib.textutil import parse_file_size
import tempfile
import os

try:
    import magic
except:
    pass

def ensure_unicode_anytype(s):
    if isinstance(s, basestring):
        return ensure_unicode(s)
    return s

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

def check_filetype(buf, need_type):
    if ukconfig.USE_MAGIC_LIB:
        s = magic.from_buffer(buf)
    else:
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(buf)
        f.close()
        s = Popen('file "{0}"'.format(f.name), stdout=PIPE, shell=True).stdout.read()
        os.remove(f.name)
    if s.find(need_type) != -1:
        return True
    else:
        return s

def check_pdf(buf):
    return check_filetype(buf, 'PDF document')

def pdf_compress(data):
    """ take a pdf data string, return a compressed string
        compression is done using ps2pdf14 in ghostscript
    """
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    f.write(data)
    f.close()

    f2 = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    f2.close()
    ret = os.system('ps2pdf14 "{0}" "{1}"'.format(f.name, f2.name))
    if ret != 0:
        raise Exception("ps2pdf14 return error! original data in {0}".format(f.name))

    newdata = open(f2.name).read()
    os.remove(f2.name)
    os.remove(f.name)
    if len(newdata) < len(data) and check_pdf(newdata):
        log_info("Compress succeed: {0}->{1}".format(
            parse_file_size(len(data)), parse_file_size(len(newdata))))
        return newdata
    else:
        return data


if __name__ == '__main__':
    print check_filetype(open("./ukconfig.py").read(), 'PDF')

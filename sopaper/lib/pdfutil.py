#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: pdfutil.py
# Date: Mon Jan 04 02:39:11 2016 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from ..lib.textutil import filter_nonascii, parse_file_size
from ..lib.ukutil import check_file_type, check_buf_filetype
from ..uklogger import *
from .. import ukconfig

import tempfile
import os

def check_buf_pdf(buf):
    return check_buf_filetype(buf, 'PDF document')

def check_legal_pdf(buf):
    def is_exe(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)
    for d in os.environ["PATH"].split(os.pathsep):
        d = d.strip('"')
        exe = os.path.join(d, 'pdftk')
        if is_exe(exe):
            break
    else:
        log_info('pdftk not installed. Not sure if pdf file is valid!')
        return True
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(buf)
    f.close()
    ret = os.system('pdftk "{}" output /dev/null'.format(f.name))
    os.unlink(f.name)
    return ret == 0

def pdf2text(data):
    f = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    f.write(data)
    f.close()

    #with timeout(seconds=30):
    ret = os.system('pdftotext "{0}"'.format(f.name))
        #ret = timeout_command('pdftotext "{0}"'.format(os.path.realpath(f.name)),
                             #3)
    if ret != 0:
        #raise Exception("Timeout in pdf2text")
        raise Exception("pdftotext return error! original file: {0}".format(f.name))
    fout = f.name.replace('.pdf', '.txt')
    text = open(fout).read()

    os.remove(f.name)
    os.remove(fout)

    text = filter_nonascii(text)
    # TODO filter formulas..
    return text

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
        log_err("Compress: ps2pdf14 failed!")
        newdata = None
    else:
        newdata = open(f2.name).read()
    file_succ = newdata is not None and \
            check_file_type(f2.name, 'PDF document') and \
            len(newdata) >= ukconfig.FILE_SIZE_MINIMUM
    try:
        os.remove(f2.name)
        os.remove(f.name)
    except OSError:
        pass
    if file_succ and \
       len(newdata) < len(data):
        log_info("Compress succeed: {0}->{1}".format(
            parse_file_size(len(data)), parse_file_size(len(newdata))))
        return newdata
    else:
        return data

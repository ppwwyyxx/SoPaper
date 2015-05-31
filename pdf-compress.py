#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: pdf-compress.py
# Date: Mon Jun 01 01:32:07 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import sys
import os
import os.path
import argparse
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'common'))

from lib.pdfutil import pdf_compress

def get_args():
    desc = 'Compress Pdf By ps2pdf'
    parser = argparse.ArgumentParser(description = desc)

    parser.add_argument('file', help='file name')
    ret = parser.parse_args()
    return ret

def main():
    global args
    args = get_args()
    data = open(args.file).read()
    newdata = pdf_compress(data)

    if len(newdata) < len(data):
        newfilename = args.file + '.compressed'
        with open(newfilename, 'w') as fout:
            fout.write(newdata)
        os.remove(args.file)
        os.rename(newfilename, args.file)

if __name__ == '__main__':
    main()

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: pdf2html.py
# Date: Mon May 26 15:43:21 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import os
import os.path
import tempfile
import shutil

class PDF2Html(object):
    def __init__(self, data, filename):
        """ provide either data or filename"""
        if data is not None:
            f = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            f.close()
            with open(f.name, 'w') as fpdf:
                fpdf.write(data)
            self.fname = f.name
            self.createfile = True
        else:
            self.fname = filename
            self.createfile = False
        assert self.fname is not None
        self.convert()

    def convert(self):
        self.outdir = tempfile.mkdtemp(prefix='sop')
        ret = os.system('pdf2htmlEX "{0}" 0.html --dest-dir={1} --zoom=1.5'.
                  format(self.fname, self.outdir) + \
                  ' --split-pages=1 --page-filename %d.html')
        if ret != 0:
            raise Exception("pdf2htmlEx return error! original file: {0}".format(self.fname))
        self.npages = len(os.listdir(self.outdir)) - 1

    def clean(self):
        shutil.rmtree(self.outdir)
        if self.createfile:
            os.remove(self.fname)

    def get_npages(self):
        return self.npages

    def get(self, t):
        t = int(t)
        assert t >= 0 and t <= self.npages
        fname = os.path.join(self.outdir, '{0}.html'.format(t))
        return open(fname).read()

if __name__ == '__main__':
    w = PDF2Html(data=None, filename='/tmp/a.pdf')
    print len(w.get(1))
    w.clean()




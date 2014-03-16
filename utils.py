#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: utils.py
# Date: Sun Mar 16 21:25:23 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

from subprocess import Popen, PIPE
def check_filetype(f, _type):
    s = Popen('file "{0}"'.format(f), stdout=PIPE, shell=True).stdout.read()
    print s
    if s.find(_type) != -1:
        return True
    else:
        return False


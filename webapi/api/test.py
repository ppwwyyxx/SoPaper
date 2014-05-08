#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: test.py
# $Date: Mon Mar 24 16:23:54 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""test with user id"""

from . import api_method, request


@api_method('/test')
def test():
    """given user id and return all items"""
    uid = request.values.get('uid')
    if not uid:
        return {'error': 'please visit with uid=1'}
    return {'data': 'hi world {0}'.format(uid)}

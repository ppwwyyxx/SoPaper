#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: indexer.py
# Date: Thu May 22 13:46:30 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import os
import xapian
from xapian import Stem, TermGenerator, Document

from xpcommon import FIELD_NUM


class XapianIndexer(object):

    def __init__(self, dirname):
        self.dbPath = os.path.abspath(dirname)
        try:
            os.mkdir(self.dbPath)
        except:
            pass

        self.db = xapian.WritableDatabase(self.dbPath,
                                         xapian.DB_CREATE_OR_OPEN)

        self.indexer = TermGenerator()
        self.indexer.set_stemmer(Stem('english'))

    def add_doc(self, doc):
        """ doc: a dict """

        content = doc['content']
        document = Document()
        document.set_data(content)

        for k, v in doc.iteritems():
            if k == 'content':
                continue
            field_num = FIELD_NUM[k]
            document.add_value(field_num, str(v))

        self.indexer.set_document(document)
        self.indexer.index_text(content)
        self.db.add_document(document)

    def flush(self):
        self.db.flush()

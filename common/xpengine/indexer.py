#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: indexer.py
# Date: Thu May 22 15:23:33 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import os
import threading
import xappy
from xappy import IndexerConnection, FieldActions, UnprocessedDocument, Field
from xappy import errors

from xpcommon import FIELD_NUM, STOPWORDS
from lib.singleton import Singleton

class XapianIndexer(object):
    __metaclass__ = Singleton

    def __init__(self, dirname):
        self.dbPath = os.path.abspath(dirname)

        self.dbconn = IndexerConnection(self.dbPath)

        self.dbconn.add_field_action('title', FieldActions.INDEX_FREETEXT,
                                     weight=5, language='en')
        self.dbconn.add_field_action('text', FieldActions.INDEX_FREETEXT,
                                     language='en', spell=True)
        self.dbconn.add_field_action('author', FieldActions.INDEX_FREETEXT,
                                     language='en')

        self.lock = threading.Lock()

        for k in FIELD_NUM.keys():
            self.dbconn.add_field_action(k, FieldActions.STORE_CONTENT)

    def add_doc(self, doc):
        """ doc: a dict """
        content = doc['text']
        document = UnprocessedDocument()
        document.fields.append(Field('text', content))

        for k, v in doc.iteritems():
            if k in ['text', 'id']:
                continue
            if type(v) == list:
                for item in v:
                    document.fields.append(Field(k, str(item)))
            else:
                document.fields.append(Field(k, str(v)))
        document.id = str(doc['id'])
        try:
            self.lock.acquire()
            self.dbconn.add(document)
        except errors.IndexerError as e:
            print str(e)
        finally:
            self.lock.release()



    def flush(self):
        self.dbconn.flush()

    def close(self):
        self.dbconn.close()

#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: indexer.py
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

__all__ = ['xapian_indexer']

import os
import threading
import shutil
import xappy
from xappy import IndexerConnection, FieldActions, UnprocessedDocument, Field
from xappy import errors
from lib.ukutil import ensure_unicode_anytype as ensure_unicode

from xpcommon import FIELD_NUM, STOPWORDS

class XapianIndexer(object):

    def __init__(self, dirname):
        self.dbPath = os.path.abspath(dirname)

        self.dbconn = IndexerConnection(self.dbPath)

        self.dbconn.add_field_action('title', FieldActions.INDEX_FREETEXT,
                                     weight=5, language='en')
        self.dbconn.add_field_action('text', FieldActions.INDEX_FREETEXT,
                                     language='en', spell=True, stop=STOPWORDS)
        #self.dbconn.add_field_action('citecnt', FieldActions.FACET, type='float')
        #self.dbconn.add_field_action('citecnt', FieldActions.WEIGHT)

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
                    document.fields.append(Field(k, ensure_unicode(item)))
            else:
                document.fields.append(Field(k, ensure_unicode(v)))
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

    def clear(self):
        self.close()
        shutil.rmtree(self.dbPath)
        self.__init__(self.dbPath)

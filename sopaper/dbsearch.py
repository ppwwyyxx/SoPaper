#!../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: dbsearch.py
# Date: 六 6月 14 03:18:57 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import operator

from .ukdbconn import get_mongo
from .uklogger import *
from .lib.textutil import title_beautify, levenshtein

SEARCH_RETURN_FIELDS = {'view_cnt': 1, 'download_cnt': 1,
                        'title': 1, 'page': 1, 'source': 1,
                        'page_url': 1,
                        'author': 1, 'bibtex': 1, 'abstract': 1,
                        'references': 1, 'citedby': 1,
                        'comments': {'$slice': 10},
                        'cmt_count': 1}

def beautify_results():
    def wrap(func):
        def call(query):
            res = func(query.lower())
            for k in res:
                k['title'] = title_beautify(k['title'])
            return res
        return call
    return wrap

@beautify_results()
def search_exact(query):
    db = get_mongo('paper')
    res = list(db.find({'title': query}, SEARCH_RETURN_FIELDS))
    return res

@beautify_results()
def search_startswith(query):
    db = get_mongo('paper')
    res = list(db.find({'title':
                        {'$regex': '^{0}'.format(query) } },
                       SEARCH_RETURN_FIELDS))
    res = [k for k in res if levenshtein(k['title'], query) < 10]
    print(res)
    return res

@beautify_results()
def search_regex(regex):
    db = get_mongo('paper')
    res = list(db.find({'title': {'$regex':
                                  '{0}'.format(query) }
                       }, SEARCH_RETURN_FIELDS))
    return res


# XXX Hack!!
# Similar Search in cached memory

all_titles = []
def similar_search(query):
    """ return one result that is most similar to query"""
    ret = []
    query = query.strip().lower()
    for cand in all_titles:
        dist = levenshtein(query, cand[0])
        if dist < 3:
            ret.append((cand, dist))
    if not ret:
        return None
    res = max(ret, key=operator.itemgetter(1))

    db = get_mongo('paper')
    res = db.find_one({'_id': res[0][1]}, SEARCH_RETURN_FIELDS)
    return res


def add_title_for_similar_search(cand):
    """ cand = (title, id) """
    all_titles.append((cand[0].strip().lower(), cand[1]))

def init_title_for_similar_search():
    if len(all_titles) > 0:
        return
    db = get_mongo('paper')
    itr = db.find({}, {'title': 1})
    for cand in itr:
        add_title_for_similar_search((cand['title'], cand['_id']))

init_title_for_similar_search()

if __name__ == '__main__':
    print(search_exact(title_beautify('Intriguing properties of neural networks')))

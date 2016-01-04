#!../../manage/exec-in-virtualenv.sh
# -*- coding: UTF-8 -*-
# File: textutil.py
# Date: Wed Jul 08 22:33:24 2015 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import string
import re
import os
import hashlib
from .ukutil import ensure_unicode

STOPWORDS = set(['of', 'from', 'as', 'to', 'a', 'an', 'in', 'into', 'on',
                 'onto', 'with', 'about', 'the', 'for', 'and', 'or', 'by',
                 'without', 'instead', 'is', 'are', 'since', 'between',
                 'after', 'befoer', 'then', 'than', 'via'])

ABBR_DICT = [(k, v) for k, v in
            [l.strip().split('\t') for l in open(os.path.join(
                os.path.dirname(__file__), 'abbr.dic')).readlines()]]

def title_beautify(title):
    title = title.strip().lower()
    title = " ".join(title.split())
    tk = title.title().split()
    for (idx, w) in enumerate(tk):
        if w.lower() in STOPWORDS and not idx == 0:
            tk[idx] = w.lower()
        else:
            tk[idx] = w.capitalize()
    return " ".join(tk)

def parse_file_size(size):
    if size > 1048576:
        return "{0:.2f}MB".format(float(size) / 1024 / 1024)
    if size > 1024:
        return "{0:.2f}KB".format(float(size) / 1024)
    return "{0}B".format(size)

def filter_title_fileformat(title):
    title = title.replace('[pdf]', '')
    title = title.replace('[PDF]', '')
    return title

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def title_correct(query, title):
    """ return (match, update) """
    title = title.replace('[PDF]', '')
    q = ''.join([t for t in query if t in string.letters]).lower()
    now = ''.join([t for t in title if t in string.letters]).lower()
    ed_thres = min(len(query), len(title)) / 5
    ERROR_RATIO = 0.6
    if levenshtein(q, now) < ed_thres:
        return (True, True)
    for k in range(min([int(len(query) * ERROR_RATIO), 30]), len(query)):
        if levenshtein(q[:k], now) < ed_thres:
            return (True, False)
    for k in range(int(len(title) * ERROR_RATIO), len(title)):
        if levenshtein(now[:k], q) < ed_thres:
            return (True, False)
    return (False, False)

def name_clean(name):
    p = re.compile('\(.*?\)', re.DOTALL)
    ret = p.sub('', name).strip()
    return ensure_unicode(ret)

def filter_nonascii(string):
    return filter(lambda x: ord(x) < 128, string)

def abbr_subst(s):
    for k, v in ABBR_DICT:
        s = re.sub(k, v, s, flags=re.IGNORECASE)
    return s

def finalize_filename(s):
    s = s.replace('/', ' ')
    s = abbr_subst(s)
    return s

def md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

if __name__ == '__main__':
    print title_correct("Gated Softmax Classification",
                        "[PDF]Gated Softmax Classification - NIPS Proceedings")

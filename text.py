#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: text.py
# Date: Mon Mar 17 11:41:36 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

import string
stopwords = set(['of', 'from', 'as', 'to', 'a', 'an', 'in', 'into', 'on',
                 'onto', 'with', 'about', 'the', 'for', 'and', 'or', 'by',
                 'without', 'instead', 'is', 'are', 'since', 'between',
                 'after', 'befoer', 'then', 'than'])

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

def title_beautify(title):
    tk = title.title().split()
    for (idx, w) in enumerate(tk):
        if w.lower() in stopwords and not title.startswith(w):
            tk[idx] = w.lower()
        else:
            tk[idx] = w.capitalize()
    return " ".join(tk)

def parse_file_size(size):
    if size > 1000000:
        return "{0:.2f}MB".format(float(size) / 1000000)
    if size > 1000:
        return "{0:.2f}KB".format(float(size) / 1000)
    return "{0}B".format(size)

def title_correct(query, title):
    q = ''.join([t for t in query if t in string.letters])
    for k in range(len(query) / 2, len(query)):
        now = ''.join([t for t in title if t in string.letters]).lower()
        if levenshtein(q[:k], now) < 7:
            return True
    return False

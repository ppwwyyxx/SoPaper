#!/bin/bash -e
# File: rebuild-index.sh
# Date: Sat May 24 11:00:06 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

PROG_NAME=`readlink -f "$0"`
PROG_DIR=`dirname "$PROG_NAME"`
cd "$PROG_DIR"

../common/contentsearch.py

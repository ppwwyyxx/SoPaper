#!/bin/bash -e
# File: clean-db.sh
# Date: Sat May 24 11:26:04 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>


PROG_NAME=`readlink -f "$0"`
PROG_DIR=`dirname "$PROG_NAME"`
cd "$PROG_DIR"

mongo sopaper --quiet <<< "
db.paper.count();
db.dropDatabase()"

./rebuild-index.sh

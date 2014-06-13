#!/bin/bash
# File: run-list.sh
# Date: 二 6月 10 04:33:59 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

while read title; do
	echo $title
	timeout 300 ../common/queryhandler.py "$title"
	echo "Done! Press Ctrl-C to stop"
	sleep 1
done < ~/less.txt

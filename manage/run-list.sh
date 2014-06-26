#!/bin/bash
# File: run-list.sh
# Date: 五 6月 13 18:38:18 2014 +0000
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

while read title; do
	echo $title
	timeout 300 ../common/queryhandler.py "$title"
	echo "Done! Press Ctrl-C to stop"
	sleep 0.5
done < ~/dm-list.txt

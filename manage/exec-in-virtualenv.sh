#!/bin/bash -e
# $File: exec-in-virtualenv.sh
# $Date: Thu May 22 15:12:40 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

# start a python script in virtualenv, with appropriate envrionment variables
# set

source $(dirname $0)/setenv.sh

if [ -z "$1" ]
then
	echo "usage: $0 <python script>"
	exit
fi

python "$@"


#!/bin/bash -e
# File: check-style.sh
# Date: Thu May 08 10:16:54 2014 +0800
# Author: Yuxin Wu <ppwwyyxxc@gmail.com>

[[ -n $ZSH_VERSION ]] && script_dir=$(dirname $0) || script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/setenv.sh

pep8=pep8
type $pep8 2> /dev/null || pep8=pep8-python2		# for archlinux

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ `uname` = 'Darwin' ]
then
  real_dir=$(realpath $script_dir)/..
else
  real_dir=$(readlink -f $script_dir)/..
fi

$pep8 $real_dir --exclude=.env,.git,bin,lib --statistics


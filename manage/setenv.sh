#!/bin/bash -e
# $File: setenv.sh
# $Date: Thu May 22 15:00:35 2014 +0800
# $Author: jiakai <jia.kai66@gmail.com>

# zsh compatibility when direct sourcing from shell
[[ -n $ZSH_VERSION ]] && script_dir=$(dirname $0) || script_dir=$(dirname ${BASH_SOURCE[0]})
source $script_dir/config.sh

realpath() {
  [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

if [ `uname` = 'Darwin' ]
then
  project_root=`realpath $script_dir/..`
else
  project_root=$(readlink -f $script_dir/..)
fi

env_dir=$project_root/.env

if [ ! -d "$env_dir" ]
then
	echo "$env_dir not found; please first run 'quickinstall'"
fi

. $env_dir/bin/activate


# zsh compatibility
[[ -n $ZSH_VERSION ]] && set -o shwordsplit

for i in $sopapermodules
do
	PYTHONPATH=$PYTHONPATH:$project_root/$i
done
export PYTHONPATH=$PYTHONPATH:$project_root

DEBIAN_PYTHON_PATH=/usr/lib/python2.7/dist-packages
[[ -d $DEBIAN_PYTHON_PATH ]] && export PYTHONPATH=$PYTHONPATH:$DEBIAN_PYTHON_PATH

if [ `uname` = 'Darwin' ]
then
  export SOPAPER_CONFIG=$(realpath -f $script_dir)
else
  export SOPAPER_CONFIG=$(readlink -f $script_dir)
fi


#!/usr/bin/env bash

set -e

target_dir=${1}
source_file=${2}
target_file=${target_dir}/`echo $(basename ${source_file}) | sed 's%\([^.]*\).*%\1%'`
cat ${source_file} | grep 'lookup(\"' | sed 's%.*lookup("\([^"]*\).*%\1%g' | sort --ignore-case | uniq > ${target_file}.txt
diff --ignore-space-change ${target_file}.ref ${target_file}.txt || (cat ${target_file}.txt && exit 1)

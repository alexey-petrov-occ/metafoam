#!/usr/bin/env bash

set -e

viscosity_dir=${1}
viscosity_file=${2}
target_file=${viscosity_dir}/`echo $(basename ${viscosity_file}) | sed 's%\([^.]*\).*%\1%'`
cat ${viscosity_file} | grep 'lookup(\"' | sed 's%.*lookup("\([^"]*\).*%\1%g' | sort --ignore-case | uniq > ${target_file}.txt
diff --ignore-space-change ${target_file}.ref ${target_file}.txt || (cat ${target_file}.txt && exit 1)

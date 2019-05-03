#!/usr/bin/env bash
set -e

models_dir=${1}
target_model=${2}
target_file=${3}

(cd ${models_dir} && basename -a $(grep -Ril -E "public ${target_model}" .) | sed 's%\([^.]*\).*%\1%g' | sort --ignore-case) > ${target_file}.txt

diff --ignore-space-change ${target_file}.ref ${target_file}.txt || (cat ${target_file}.txt && exit 1)

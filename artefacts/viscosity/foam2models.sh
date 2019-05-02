#!/usr/bin/env bash
set -e

foam=${1}

dir=$(cd `dirname $0` && pwd)
source ${dir}/env.sh

transportModels_dir=${foam}/src/transportModels
(cd ${transportModels_dir} && basename -a $(grep -Ril -E 'public viscosityModel' .) | sed 's%\([^.]*\).*%\1%g' | sort --ignore-case) > ${viscosity_file}.txt

diff --ignore-space-change ${viscosity_file}.ref ${viscosity_file}.txt || (cat ${viscosity_file}.txt && exit 1)

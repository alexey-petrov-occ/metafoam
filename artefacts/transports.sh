#!/usr/bin/env bash

set -e

viscosity_out=${1}
transportModels_dir=${2}
viscosity_dir=${3}
cat ${viscosity_out} | while read file; do find ${transportModels_dir} -name ${file}.C -exec artefacts/transport.sh ${viscosity_dir} {} + ; done

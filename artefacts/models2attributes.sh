#!/usr/bin/env bash
set -e

list_of_models=${1}
models_source_dir=${2}
output_dir=${3}
cat ${list_of_models} | while read model; do find ${models_source_dir} -name ${model}.C -exec artefacts/extract_attributes.sh ${output_dir} {} + ; done

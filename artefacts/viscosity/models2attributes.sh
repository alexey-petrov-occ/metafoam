#!/usr/bin/env bash

set -e

foam=${1}

dir=$(cd `dirname $0` && pwd)

source ${dir}/env.sh

artefacts/models2attributes.sh ${viscosity_file} ${transportModels_dir} ${viscosity_dir}

#!/usr/bin/env bash
# Script to clean the Merlin scratch nodes
# 
# 20160406

# Get the base directory of the argument.
# Can resolve single symlinks if readlink is installed
function scriptdir {
    cd "$(dirname "$1")"
    cd "$(dirname "$(readlink "$1" 2>/dev/null || basename "$1" )")"
    pwd
}
# Bootstrap locating config directory
: "${PIPELINE_ROOT:=$(scriptdir "$(scriptdir "$0")/../../.")}"

# load config variables and passwords
source "${PIPELINE_ROOT}/config/credentials.conf" || exit
source "${PIPELINE_ROOT}/config/pipeline.conf" || exit

# Required parameters
: ${SCRATCH_UNIPROT:?Not configured}
: ${HOSTS_LIST}:?Not configured}


echo "Removing content of "${SCRATCH_UNIPROT}" directories on the merlinc nodes"

"${PIPELINE_ROOT}/scripts/pipeline/sge/rm_folder_nodes.sh" -f "${SCRATCH_UNIPROT}" -l "${HOSTS_LIST}"


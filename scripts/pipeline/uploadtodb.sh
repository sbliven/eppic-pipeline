#!/usr/bin/env bash
# Upload to the database

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
source "${PIPELINE_ROOT}/config/credentials.conf"
source "${PIPELINE_ROOT}/config/pipeline.conf"

# Required parameters
: "${EPPIC_DB:?Not configured}"
: "${WUI_FILES:?Not configured}"
if [[ ! -e "${EPPIC_DB_JAR:?Not configured}" ]]; then echo "$EPPIC_DB_JAR not found" >&2; exit 1; fi

# Execute
echo exec java -jar "$EPPIC_DB_JAR" UploadToDb -D "$EPPIC_DB" -d "$WUI_FILES" -l



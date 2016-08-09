#!/usr/bin/env bash
# Template for EPPIC scripts to include configuration files

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
: "${JETTY_BASE:?Not configured}"
if [[ ! -e "${EPPIC_CLI_JAR:?Not configured}" ]]; then echo "ERROR: $EPPIC_CLI_JAR not found" >&2; exit 1; fi
if [[ ! -e "${EPPIC_DB_JAR:?Not configured}" ]]; then echo "ERROR: $EPPIC_DB_JAR not found" >&2; exit 1; fi
: ${MYSQL_HOST:=127.0.0.1}
: "${DB_PASSWORD:?Not configured}"
: "${DB_USER:?Not configured}"

usage=$(cat - <<ENDUSAGE
usage: $0 [OPTIONS] input_list

ARGUMENTS
=========

  input_list: A file containing the list of structures to run, or a single structure ID
  
OPTIONS
=======

  -f    Force recomputation. Discards existing files and database.
ENDUSAGE
)


# Check bash version
if ((BASH_VERSINFO[0] < 4))
then 
  echo "Sorry, you need at least bash-4.0 to run this script." 
  exit 1 
fi

# parse arguments
force=
case "$1" in
    -h)
        echo "$usage"
        exit 0
        ;;
    -f)
        force=1
        shift
        ;;
    -*)
        echo "$usage" >&2
        echo "Unknown option $1" >&2
        exit 1
        ;;
esac

if [[ "$#" -lt 1 ]]; then
    echo "$usage" >&2
    echo "Not enough arguments"
    exit 1
fi

inputlist="$1"
shift

if [[ "$#" -gt 0 ]]; then
    echo "$usage" >&2
    echo "Too many arguments"
    exit 1
fi


# read inputs
declare -a structures
if [[ -f "$inputlist" ]]; then
    readarray -t structures < <(grep -v "^#" "$inputlist")
elif [[ ${#inputlist} = 4 ]]; then
    structures[0]=$inputlist
else
    echo "Unable to find $inputlist" >&2
    exit 1
fi

# Database must be created externally
while [[ -z "$(mysql -h "${MYSQL_HOST}" -u "${DB_USER}" --password="${DB_PASSWORD}"<<<"show databases like \"${EPPIC_DB}\";")" ]]; do
    cat - <<END
No database. Please run in mysql as root, substituting the correct user and host:

    CREATE DATABASE \`${EPPIC_DB}\`;
    GRANT ALL PRIVILEGES ON \`${EPPIC_DB}\`.* TO 'eppicweb'@'localhost';

>
END
    read ack
done

# -f: remove prior output
if [[ -n "$force" ]]; then
    rm -rf "${WUI_FILES}"
    mysql -h "${MYSQL_HOST}" -u "${DB_USER}" --password="${DB_PASSWORD}" "${EPPIC_DB}" <<END
SET FOREIGN_KEY_CHECKS = 0;
SET GROUP_CONCAT_MAX_LEN=32768;
SET @tables = NULL;
SELECT GROUP_CONCAT('\`', table_name, '\`') INTO @tables
  FROM information_schema.tables
  WHERE table_schema = (SELECT DATABASE());
SELECT IFNULL(@tables,'dummy') INTO @tables;

SET @tables = CONCAT('DROP TABLE IF EXISTS ', @tables);
PREPARE stmt FROM @tables;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
SET FOREIGN_KEY_CHECKS = 1;
END
fi

# Loop over inputs
for pdb in "${structures[@]}"; do
    echo "'${pdb}'"

    # prepare static file location
    outdir="${WUI_FILES}/divided/${pdb:1:2}/$pdb"
    mkdir -p "$outdir"
    
    # Run EPPIC
    if [[ ! -f "$outdir/finished" ]]; then
        java -Xmx3g -Xmn1g -cp "$EPPIC_CLI_JAR" eppic.Main -i "$pdb" -a 1 -o "$outdir" -w -l -P -p #-s
    fi
done

# Upload to DB
if [[ -a "$inputlist" ]]; then
    java -jar "$EPPIC_DB_JAR" UploadToDb -D "${EPPIC_DB}" -d "$WUI_FILES" \
        -l -f "$inputlist"
else
    java -jar "$EPPIC_DB_JAR" UploadToDb -D "${EPPIC_DB}" -d "$WUI_FILES" \
        -l -f <(echo "$inputlist")
fi
# java -jar /home/eppicweb/software/jars/eppic-dbtools.jar ClusterSequences -D ${EPPIC_DB} -a 8

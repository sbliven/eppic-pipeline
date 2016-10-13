#!/usr/bin/env bash
# Runs or creates a docker container for the eppic mysql database.  Existing
# containers are started if found, and the current eppic database is created if
# needed and configured. Note that the mysql root credentials must be defined
# in credentials.conf and must match the existing database at $MYSQL_DATA, if
# any.


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
: "${DOCKER:=$(which docker)}"
: "${DOCKER:?Docker not installed or DOCKER not configured}"
: "${DOCKER_DB_CONTAINER:?Not configured}"
: "${MYSQL_DATA:?Not configured}"
: "${DB_USER:?Not configured}"
: "${DB_PASSWORD:?Not configured}"
: "${DB_ROOT_PASSWORD:?Not configured}"
: "${EPPIC_DB:?Not configured}"
: "${UNIPROT_DB:?Not configured}"


# Check for existing containers
RUNNING=$($DOCKER inspect -f '{{.State.Running}}' "$DOCKER_DB_CONTAINER" 2>/dev/null)
if [ $? -eq 1 ]; then
    # Container didn't exist
    echo "Creating new docker container '$DOCKER_DB_CONTAINER' to run the database"
    mkdir -p "$MYSQL_DATA" || exit $?

    # Create new container for the database, with data stored at $MYSQL_DATA
    $DOCKER run \
        --detach \
        --name "$DOCKER_DB_CONTAINER" \
        --volume "$MYSQL_DATA:/var/lib/mysql" \
        --env MYSQL_USER="${DB_USER}" \
        --env MYSQL_PASSWORD="${DB_PASSWORD}" \
        --env MYSQL_ROOT_PASSWORD="${DB_ROOT_PASSWORD}" \
        --publish 3306:3306 \
        mysql:5.7

        #--env MYSQL_DATABASE="${EPPIC_DB}" \
        #--env MYSQL_RANDOM_ROOT_PASSWORD=yes \
elif [ "$RUNNING" == "false" ]; then
    # Container was stopped
    echo "Starting docker container '$DOCKER_DB_CONTAINER' to run the database"
    $DOCKER start "$DOCKER_DB_CONTAINER"
else
    echo "Docker container '$DOCKER_DB_CONTAINER' already running the database"
fi

# Wait for the database to initialize
echo Waiting for database to start
timeout 45 bash <<END
# Wait for port to open
while ! (echo > /dev/tcp/127.0.0.1/3306) >/dev/null 2>&1
do
    sleep 1
done
# Wait for mysql to start
while ! (mysqladmin ping -h 127.0.0.1 -u root --password=$"DB_ROOT_PASSWORD") >/dev/null 2>&1
do
    sleep 1
done
END
if [ $? -eq 0 ]; then
    echo "Database running"
else
    echo "ERROR: Database timed out!" >&2
    exit 1
fi

# Create databases
mysql -h 127.0.0.1 -u root --password="$DB_ROOT_PASSWORD" <<END
CREATE DATABASE IF NOT EXISTS \`${EPPIC_DB}\`;
CREATE DATABASE IF NOT EXISTS \`${UNIPROT_DB}\`;
GRANT ALL ON \`${EPPIC_DB}\`.* to \`$DB_USER\`@\`%\`;
GRANT ALL ON \`${UNIPROT_DB}\`.* to \`$DB_USER\`@\`%\`;
END
if [ $? != 0 ]; then
    echo "ERROR configuring mysql databases" >&2; exit 1;
fi

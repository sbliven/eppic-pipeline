#!/bin/bash

# load config variables and passwords
source credentials.conf
source pipeline.conf

RUNNING=$($DOCKER inspect -f '{{.State.Running}}' "$DOCKER_DB_CONTAINER" 2>/dev/null)
if [ $? -eq 1 ]; then
    # Container didn't exist
    echo "Creating new docker container '$DOCKER_DB_CONTAINER' to run the database"
    mkdir -p "$MYSQL_DATA" || exit $?
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

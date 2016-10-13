#!/bin/bash

# Script to upload chunk into eppicdb
# To be used after chunk transfer to eppic01 is complete
# 20151103

DATABASE_DATE="2015_12"

if [ -z "$1" ]; then
echo "No chunk number given. Usage: ./upload_chunk_topup.sh [chunk_number]"
exit
fi

echo "Using -F flag"

/usr/bin/java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UploadToDb -D eppic_2015_12_2 -d /data/webapps/files_$DATABASE_DATE \
-l -f /data/webapps/files_$DATABASE_DATE/input/pdbchunk$1_run0.list -F

exit


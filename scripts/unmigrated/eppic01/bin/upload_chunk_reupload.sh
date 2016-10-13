#!/bin/bash

# Script to upload chunk into eppicdb
# To be used after chunk transfer to eppic01 is complete
# 20150927

DATABASE_DATE="2015_12"

if [ -z "$1" ]; then
echo "No chunk number given. Usage: ./upload_chunk.sh [chunk_number]"
exit
fi

/usr/bin/java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UploadToDb -D eppic_2015_12_2 -d /data/webapps/files_$DATABASE_DATE \
-l -f /data/webapps/files_$DATABASE_DATE/input/pdbchunk$1_run0.list

exit


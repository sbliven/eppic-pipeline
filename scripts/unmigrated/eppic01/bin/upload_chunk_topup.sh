#!/bin/bash

# Script to upload chunk into eppicdb
# To be used after chunk transfer to eppic01 is complete
# 20151103

DATABASE_DATE="2016_05"

if [ -z "$1" ]; then
echo "No chunk number given. Usage: ./upload_chunk_topup.sh [chunk_number]"
exit
fi

#rm -f transfer_${DATABASE_DATE}_chunk$1.log
#rsync -avz $HOME/eppic_$DATABASE_DATE/output/chunk$1/data/divided eppicweb@eppic01:/bigdata/files_$DATABASE_DATE/ 2>&1 | tee $HOME/transfer_${DATABASE_DATE}_chunk$1.log

echo "Using -F flag"

/usr/bin/java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UploadToDb -D eppic_$DATABASE_DATE -d /data/webapps/files_$DATABASE_DATE \
-l -f /data/webapps/files_$DATABASE_DATE/input/pdbchunk$1_run0.list -F

exit


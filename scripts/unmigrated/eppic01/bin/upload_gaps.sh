#!/bin/bash

# Script to upload gaps.list into eppicdb
# 20150929

DATABASE_DATE="2015_09"

if [ ! -f /data/webapps/files_$DATABASE_DATE/input/gaps.list ]; then
echo "No gaps.list file in /data/webapps/files_$DATABASE_DATE/input/"
exit
fi

echo "Gaps.list file found in /data/webapps/files_$DATABASE_DATE/input/, proceeding with upload"

/usr/bin/java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UploadToDb -D eppic_$DATABASE_DATE -d /data/webapps/files_$DATABASE_DATE \
-l -F -f /data/webapps/files_$DATABASE_DATE/input/gaps.list

exit


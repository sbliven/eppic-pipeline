#!/bin/bash

# Script to check precomputation for a given db
# To be used after chunk transfer to eppic01 and upload is complete
# 20160405

if [ -z "$1" ]; then
echo "No database version given. Usage: ./precomp_check.sh [database_date_as YYYY_MM]"
exit
fi

mkdir /home/eppicweb/precomp_check/$1
python /home/eppicweb/bin/CheckDatabase.py eppic_$1 /home/eppicweb/precomp_check/$1

java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UploadToDb -D eppic_$1 -d /data/webapps/files_$1 -l -f /home/eppicweb/precomp_check/$1/obsolete.list -r

exit


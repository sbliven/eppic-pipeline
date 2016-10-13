#!/bin/bash

# Script to check precomputation for a given db
# To be used after chunk transfer to eppic01 and upload is complete
# 20160505


if [ -z "$1" ]; then
echo "No database version given. Usage: ./cluster_sequences.sh [database_date_as YYYY_MM]"
exit
fi

java -jar /home/eppicweb/software/jars/eppic-dbtools.jar ClusterSequences -D eppic_$1 -a 8

exit


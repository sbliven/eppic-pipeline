#!/bin/bash

# Script run eppic after blast_cache step
# 20150922

DATABASE_DATE="2016_07"

if [ -z "$1" ]; then
echo "No chunk number given. Usage: ./check_run_cycle.sh [chunk_number]"
exit
fi

echo "Checking chunk completion for run ${DATABASE_DATE}, chunk $1"

/usr/bin/python /gpfs/home/capitani/eppic-pipeline/src/EPPICpipeline/EPPICrun.py /gpfs/home/capitani/eppic_${DATABASE_DATE} 1 $1 

if test -f "/gpfs/home/capitani/eppic_${DATABASE_DATE}/qsubscripts/eppic_chunk$1_run1.sh"; 

then

echo "Run file exists, submitting run1"

/gpfs/home/gridengine/sge6.2u5p2/bin/lx26-amd64/qsub /gpfs/home/capitani/eppic_${DATABASE_DATE}/qsubscripts/eppic_chunk$1_run1.sh

else

echo "All jobs finished, starting transfer to eppic01"

rm -f $HOME/transfer_${DATABASE_DATE}_chunk$1.log

rsync -avz $HOME/eppic_$DATABASE_DATE/output/chunk$1/data/divided eppicweb@eppic01:/bigdata/files_$DATABASE_DATE/ 2>&1 | tee $HOME/transfer_logs/transfer_${DATABASE_DATE}_chunk$1.log

fi


exit

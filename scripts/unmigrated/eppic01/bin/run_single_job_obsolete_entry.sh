#!/bin/bash

# Script to run single job to fill gap in precomp from merlin
# 20160607


if [ -z "$1" ]; then
echo "No pdb entry given.  Usage: ./run_single_job_obsolete_entry.sh [entry_code]"
exit
fi

#mid_pdb=`echo $1 | awk -F "" '{print $2$3}'`

#echo $mid_pdb
#echo "Entry code:" $1

cd /home/eppicweb/test/z2/1z2r/
/home/eppicweb/software/bin/eppic -i 1z2r -a 1 -s -o /home/eppicweb/test/z2/1z2r \
-l -w -g /home/eppicweb/.eppic_2016_04.conf

exit


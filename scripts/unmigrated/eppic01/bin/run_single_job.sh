#!/bin/bash

# Script to run single job to fill gap in precomp from merlin
# 20150929


if [ -z "$1" ]; then
echo "No pdb entry given.  Usage: ./run_single_job.sh [entry_code]"
exit
fi

mid_pdb=`echo $1 | awk -F "" '{print $2$3}'`

echo $mid_pdb
echo "Entry code:" $1

/home/eppicweb/software/bin/eppic -i /home/eppicweb/topup/30-03-2016/output/data/divided/$mid_pdb/$1/$1.cif -a 1 -s -o /home/eppicweb/topup/30-03-2016/output/data/divided/$mid_pdb/$1 \
-l -w -g /home/eppicweb/.eppic.conf


exit


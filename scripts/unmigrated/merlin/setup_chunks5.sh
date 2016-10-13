#!/bin/bash

# Script to setup the chunk5 topup job on merlin
# To be used after the other chunks have been completed
# 20160304

TOPUP_DATE="22-06-2016"
DATABASE_DATE="2016_06"

#if [ -z "$1" ]; then
#echo "No topup date given. Usage: ./setup_chunk5.sh [topup date]"
#exit
#fi

rm /gpfs/home/capitani/eppic_$DATABASE_DATE/input/pdbchunk5_run0.list 
scp eppicweb@eppic01:/home/eppicweb/topup/$TOPUP_DATE/input/pdbinput_$TOPUP_DATE.list /gpfs/home/capitani/eppic_$DATABASE_DATE/input/pdbchunk5_run0.list
wc /gpfs/home/capitani/eppic_$DATABASE_DATE/input/pdbchunk5_run0.list > xxxx
read lines words characters filename < xxxx
rm xxxx
echo "Number of topup jobs=$lines"

cp /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk1_run0.sh /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh
sed s/chk1/chk5/ /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh > /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new
sed s/chunk1/chunk5/ /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new > /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new2
sed s/30000/$lines/ /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new2 > /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new3
mv /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new3 /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh
rm /gpfs/home/capitani/eppic_$DATABASE_DATE/qsubscripts/eppic_chunk5_run0.sh_new*

mkdir /gpfs/home/capitani/eppic_$DATABASE_DATE/output/chunk5 /gpfs/home/capitani/eppic_$DATABASE_DATE/output/chunk5/data /gpfs/home/capitani/eppic_$DATABASE_DATE/output/chunk5/logs
mkdir /gpfs/home/capitani/eppic_$DATABASE_DATE/output/chunk5/data/all /gpfs/home/capitani/eppic_$DATABASE_DATE/output/chunk5/data/divided

#rm -f transfer_${DATABASE_DATE}_chunk$1.log

#rsync -avz $HOME/eppic_$DATABASE_DATE/output/chunk$1/data/divided eppicweb@eppic01:/bigdata/files_$DATABASE_DATE/ 2>&1 | tee $HOME/transfer_logs/transfer_${DATABASE_DATE}_chunk$1.log

exit

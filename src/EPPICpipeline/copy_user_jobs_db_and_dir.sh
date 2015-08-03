#!/bin/bash

# script to copy user jobs to the next version of eppicdb and the user jobs files to the corresponding directories
# 150803

rm -f tmp.list
 
SOURCE_DATE="2015_06"
TARGET_DATE="2015_07"
T=40 # jobs from the last T days will be copied from old to new db

rm -f copy_eppic_files_${SOURCE_DATE}_to_eppic_${TARGET_DATE}.log

echo "User jobs are being copied from source (old) to target (new) db"
echo "Old db:" eppic_$SOURCE_DATE
echo "New db:" eppic_$TARGET_DATE

java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UserJobCopier -d /data/webapps/files_$SOURCE_DATE/ -s eppic_$SOURCE_DATE -g eppic_$TARGET_DATE -t $T | grep " Copying" > tmp.list

if [ -s tmp.list ]
then
        length=($(wc tmp.list))
        echo "Number of copied jobs:" $length
else
        echo "WARNING: List of user jobs is empty, exiting"
        exit
fi

#copy jobs files
echo "Copying user job files from eppic_${SOURCE_DATE} dir to eppic_${TARGET_DATE} dir, see log for details"
for fname in $(awk '{print $1}' "tmp.list")
do
cp -rv /data/webapps/files_$SOURCE_DATE/$fname /bigdata/eppic_$TARGET_DATE/ >> copy_eppic_files_${SOURCE_DATE}_to_eppic_${TARGET_DATE}.log
done



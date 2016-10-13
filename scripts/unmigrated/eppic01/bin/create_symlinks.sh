#!/bin/sh

if [ -z "$1" ]
then
        echo "Usage: $0 <dir to create PDB symlinks in>"
        echo "  example: $0 /data/webapps/files1"
        exit 1
fi

DESTINATION_DIR=$1

#Create symbolic links in DESTINATION_DIR

cd $DESTINATION_DIR
 
for dir in `find divided -maxdepth 3 -type d -name "????"`
do
        ln -sf $dir 
done


#!/bin/bash

# Script to update conf files to new db in merlin

DATABASE_DATE_OLD="2016_06"
DATABASE_DATE_NEW="2016_07"

echo "This script will prepare merlin for the blast run and change the db version in the .eppic.conf and Blastcache.py files" 
read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

echo "Cleaning scratch dirs on merlinc nodes"

/gpfs/home/capitani/bin/rm_folder_nodes.sh -f /scratch/capitani/uniprot_${DATABASE_DATE_OLD} -l /gpfs/home/capitani/bin/hosts.list

echo "Downloading the most recent SIFTS file"

rm $HOME/data/uniprot/pdb_chain_uniprot.lst
cd $HOME/data/uniprot/
$HOME/data/uniprot/download_shifts_file

cd $HOME/

echo "Doing the change"
   
sed s/$DATABASE_DATE_OLD/$DATABASE_DATE_NEW/ $HOME/.eppic.conf > $HOME/.eppic.conf_new
mv $HOME/.eppic.conf_new $HOME/.eppic.conf

sed s/uniprot_$DATABASE_DATE_OLD/uniprot_$DATABASE_DATE_NEW/ $HOME/eppic-pipeline/src/EPPICpipeline/BlastCache.py > $HOME/eppic-pipeline/src/EPPICpipeline/BlastCache.py_new
mv $HOME/eppic-pipeline/src/EPPICpipeline/BlastCache.py_new $HOME/eppic-pipeline/src/EPPICpipeline/BlastCache.py

fi

exit


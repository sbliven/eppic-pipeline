#!/bin/bash

# Script to clean the Merlin scratch nodes
# 
# 20160406

DATABASE_DATE="2016_07"

echo "Removing content of /scratch/capitani/uniprot_${DATABASE_DATE} directories on the merlinc nodes"

/gpfs/home/capitani/bin/rm_folder_nodes.sh -f /scratch/capitani/uniprot_${DATABASE_DATE} -l /gpfs/home/capitani/bin/hosts.list



#!/bin/bash

# Script to transfer input and blast cache to production after eppic runs
# 20160529

DATABASE_DATE="2016_07"

echo "Transferring input files for run ${DATABASE_DATE}"

rsync -avz eppic_${DATABASE_DATE}/input eppicweb@eppic01:/bigdata/files_${DATABASE_DATE} 

ssh eppicweb@eppic01 ln -s /bigdata/files_${DATABASE_DATE} /data/webapps

rsync -avz $HOME/data/blast_cache/uniprot_${DATABASE_DATE} eppicweb@eppic01:/data/dbs/blast_cache/

exit

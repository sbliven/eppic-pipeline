#!/bin/bash

# Script run eppic after blast_cache step, includes updating local pdb repo
# 20150922

DATABASE_DATE="eppic_2016_07"

echo "Launching jobs for run ${DATABASE_DATE}"

/usr/bin/python /gpfs/home/capitani/eppic-pipeline/src/EPPICpipeline/EPPICrun.py /gpfs/home/capitani/${DATABASE_DATE};
/gpfs/home/gridengine/sge6.2u5p2/bin/lx26-amd64/qsub /gpfs/home/capitani/${DATABASE_DATE}/qsubscripts/eppic_chunk1_run0.sh
/gpfs/home/gridengine/sge6.2u5p2/bin/lx26-amd64/qsub /gpfs/home/capitani/${DATABASE_DATE}/qsubscripts/eppic_chunk2_run0.sh
/gpfs/home/gridengine/sge6.2u5p2/bin/lx26-amd64/qsub /gpfs/home/capitani/${DATABASE_DATE}/qsubscripts/eppic_chunk3_run0.sh
/gpfs/home/gridengine/sge6.2u5p2/bin/lx26-amd64/qsub /gpfs/home/capitani/${DATABASE_DATE}/qsubscripts/eppic_chunk4_run0.sh
/gpfs/home/gridengine/sge6.2u5p2/bin/lx26-amd64/qsub /gpfs/home/capitani/${DATABASE_DATE}/qsubscripts/eppic_chunk5_run0.sh
exit

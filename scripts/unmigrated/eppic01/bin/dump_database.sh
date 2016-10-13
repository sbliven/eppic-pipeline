#!/bin/bash

# Script to dump a db from eppic01
# 
# 20151104

DATABASE_DATE="2016_04"

echo "Dumping db eppic_${DATABASE_DATE}"

mysqldump eppic_$DATABASE_DATE | gzip > /bigdata/eppicdb/eppic_$DATABASE_DATE_1z2r.sqldump.gz

exit


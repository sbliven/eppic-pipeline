#!/bin/bash

# Script to upload chunk into eppicdb

DATABASE_DATE="2016_04"

/usr/bin/java -jar /home/eppicweb/software/jars/eppic-dbtools.jar UploadToDb -D eppic_$DATABASE_DATE -d /home/eppicweb/test \
-l -f /home/eppicweb/test/entry.list -F

exit


#!/bin/sh
if [ -z "$1" ]
then
        echo "Usage: $0 <war file location>"
        exit 1
fi

configdir=~/server-config
warfile=$1

rm -rf /data/webapps/ewui/*
cp $warfile /data/webapps/ewui/
unzip /data/webapps/ewui/ewui.war -d /data/webapps/ewui/

# not copying these 3 anymore as they are not so changeable and anyway changes in them should come from the compiled war
#cp $configdir/orm.xml $configdir/email.properties  $configdir/grid.properties /data/webapps/ewui/WEB-INF/classes/META-INF

cp $configdir/input_parameters.xml $configdir/server.properties  $configdir/sge_queuing_system.properties /data/webapps/ewui/WEB-INF/classes/META-INF

cp $configdir/web.xml /data/webapps/ewui/WEB-INF

cp $configdir/jetty-env.xml /data/webapps/ewui/WEB-INF

ln -s /data/webapps/ewui/WEB-INF/lib/eppic-cli*.jar /data/webapps/ewui/WEB-INF/lib/eppic.jar

~/bin/restart-jetty.sh


#!/bin/sh
pkill -f "java -Xmx4g -Dorg.eclipse.jetty.LEVEL=INFO -jar start.jar etc/jetty-logging.xml"
sleep 3
cd ~/jetty
java -Xmx4g -Dorg.eclipse.jetty.LEVEL=INFO -jar start.jar etc/jetty-logging.xml &


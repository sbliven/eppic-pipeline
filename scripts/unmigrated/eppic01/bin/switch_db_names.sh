#!/bin/bash

# Script to update conf files to new db in eppic01

DATABASE_DATE_OLD="2016_04"
DATABASE_DATE_NEW="2016_05"

echo "This script will change the db version in the eppic and server config files" 
read -p "Are you sure? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then

echo "Doing to the change"
   
sed s/$DATABASE_DATE_OLD/$DATABASE_DATE_NEW/ $HOME/.eppic.conf > $HOME/.eppic.conf_new
mv $HOME/.eppic.conf_new $HOME/.eppic.conf

sed s/$DATABASE_DATE_OLD/$DATABASE_DATE_NEW/ /data/webapps/ewui/WEB-INF/jetty-env.xml > /data/webapps/ewui/WEB-INF/jetty-env.xml_new
mv /data/webapps/ewui/WEB-INF/jetty-env.xml_new  /data/webapps/ewui/WEB-INF/jetty-env.xml

sed s/$DATABASE_DATE_OLD/$DATABASE_DATE_NEW/ /data/webapps/ewui/WEB-INF/classes/META-INF/server.properties > /data/webapps/ewui/WEB-INF/classes/META-INF/server.properties_new
mv /data/webapps/ewui/WEB-INF/classes/META-INF/server.properties_new /data/webapps/ewui/WEB-INF/classes/META-INF/server.properties 

fi

exit


import pymysql
import logging
import luigi
from luigi.contrib.mysqldb import MySqlTarget

logger = logging.getLogger('luigi-interface')

def createDatabase(host, database, user, password):
    #logger.debug("Connecting mysql -h '{host}' -u '{user}' -p'{password}'".format(host=host,user=user,password="*"*len(password)))
    with pymysql.connect(user=user, host=host, passwd=password,autocommit=True) as cursor:
        # Check if the database already exists
        chkflg=cursor.execute("SHOW DATABASES like '%s'"%(database))
        if not chkflg:
            # doesn't exist
            logger.info("Creating database %s",database)
            createdb = cursor.execute("CREATE DATABASE %s"%(database))

class SafeMySqlTarget(MySqlTarget):
    def __init__(self, host, database, user, password, table, update_id, **kwargs):
        createDatabase(host, database, user, password)
        super(SafeMySqlTarget,self).__init__(host, database, user, password, table, update_id, **kwargs)

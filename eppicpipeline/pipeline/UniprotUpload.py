'''
Created on Dec 19, 2014
Eppic computation pipeline script
@author: baskaran_k
'''


from commands import getstatusoutput,getoutput
from subprocess import Popen,PIPE,call
from string import atof
import MySQLdb
import sys
from time import localtime,strftime
from urllib2 import urlopen

class ConnectionError(Exception): pass

class UniprotUpload:

    def __init__(self,outpath,version=None):
        self.uniprot= version if version else self.currentVersion()
        self.userName=getoutput('whoami') #remote user!
        self.remoteHost="merlinl01.psi.ch"
        self.remoteDir="" # home directory
        self.mysqluser='root'
        self.mysqlhost='mpc1153.psi.ch'
        self.mysqlpasswd=''
        self.outpath=outpath
        self.uniprotDatabase="uniprot_%s"%(self.uniprot)
        self.outdir="%s/eppic_%s"%(self.outpath,self.uniprot)
        self.eppicjar="%s/eppic.jar"%(self.outpath)
        self.downloadFolder="%s/download"%(self.outdir)
        self.fastaFolder="%s/unique_fasta"%(self.outdir)
        self.uniprotDir="%s/%s"%(self.outdir,self.uniprotDatabase)
        self.logfile=open("%s/uniprot_upload_%s.log"%(self.outpath,strftime("%d%m%Y",localtime())),'a')
        self.clusterFolder="%s/eppic_%s"%(self.outdir,self.uniprot)
    def writeLog(self,msg,checkpoint):
        t=strftime("%d-%m-%Y %H:%M:%S",localtime())
        self.logfile.write("%s\t%s\n"%(t,msg))
        if checkpoint: self.logfile.write("Checkpoint=%d\n"%(checkpoint))
        self.logfile.flush()
        print "%s\t%s\n"%(t,msg)

    # Definitions for database downloads

    urlSifts="ftp://ftp.ebi.ac.uk/pub/databases/msd/sifts/text/pdb_chain_uniprot.lst" #main ftp
    #urlSifts="ftp://ftp.uniprot.org/pub/databases/msd/sifts/text/pdb_chain_uniprot.lst" #UK mirror

    urlUniref100xml="ftp://ftp.expasy.org/databases/uniprot/current_release/uniref/uniref100/uniref100.xml.gz" #SWISS mirror
    #urlUniref100xml="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/uniref/uniref100/uniref100.xml.gz" #main ftp but slow

    urlUniprotReldate="ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/reldate.txt" #Swiss mirror
    #urlUniprotReldate="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/reldate.txt" # main ftp

    urlUniref100fasta="ftp://ftp.expasy.org/databases/uniprot/current_release/uniref/uniref100/uniref100.fasta.gz" #Swiss mirror
    #urlUniref100fasta="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/uniref/uniref100/uniref100.fasta.gz" #main ftp

    urlBlastdb="ftp://ftp.uniprot.org/pub" # main ftp
    #urlBlastdb="ftp://ftp.ebi.ac.uk/pub" # UK mirror

    urlTaxonomy="http://www.uniprot.org/taxonomy/?query=*&compress=yes&format=tab"

    TABLES = {}
    TABLES['uniprot'] = (
                         "CREATE TABLE `uniprot` ("
                         "`id` varchar(23),"
                         "`uniprot_id` varchar(15),"
                         "`uniparc_id` char(13) PRIMARY KEY,"
                         "`tax_id` int,"
                         "`sequence` text"
                         ")")
    TABLES['uniprot_clusters'] = (
                                  "CREATE TABLE `uniprot_clusters` ("
                                  "`representative` varchar(15),"
                                  "`member` varchar(15) PRIMARY KEY,"
                                  "`tax_id` int"
                                  ")")
    TABLES['taxonomy'] = (
                          "CREATE TABLE `taxonomy` ("
                          "`tax_id` int PRIMARY KEY,"
                          "`mnemonic` varchar(20),"
                          "`scientific` varchar(255),"
                          "`common` varchar(255),"
                          "`synonym` varchar(255),"
                          "`other` text,"
                          "`reviewed` varchar(20),"
                          "`rank` varchar(20),"
                          "`lineage` text,"
                          "`parent` int"
                          ")")


    def connectDatabase(self,overwrite=False):
        # Ignore subsequent calls
        if getattr(self,"cnx",None) is not None:
            return

        self.writeLog("INFO: Connecting to MySQL database",0)
        # Connect with no database
        try:
            self.cnx=MySQLdb.connect(user=self.mysqluser,host=self.mysqlhost,passwd=self.mysqlpasswd,local_infile=True)
            self.cursor = self.cnx.cursor()
        except Exception as e:
            self.writeLog("ERROR:Can't connect to mysql database",1)
            raise e
        # Check if the database already exists
        chkflg=self.cursor.execute("SHOW DATABASES like '%s'"%(self.uniprotDatabase))
        if chkflg:
            # exists
            self.writeLog("WARNING: Database %s already exists"%(self.uniprotDatabase),0)
            if overwrite:
                self.cursor.execute("DROP DATABASE %s"%(self.uniprotDatabase))
                createdb=self.cursor.execute("CREATE DATABASE %s"%(self.uniprotDatabase))
                self.writeLog("WARNING: %s database will be overwritten"%(self.uniprotDatabase),0)
            else:
                self.writeLog("WARNING: Using existing %s database; This may create problems if tables already exist in the database"%(self.uniprotDatabase),0)
        else:
            # doesn't exist
            createdb=self.cursor.execute("CREATE DATABASE %s"%(self.uniprotDatabase))
            self.writeLog("INFO: Connected to %s database"%(self.uniprotDatabase),0)
        self.cnx=MySQLdb.connect(user=self.mysqluser,host=self.mysqlhost,passwd=self.mysqlpasswd,db=self.uniprotDatabase,local_infile=True)
        self.cursor = self.cnx.cursor()


    def checkMemory(self):
        df = Popen(["df",self.outpath], stdout=PIPE)
        outdat=df.communicate()[0]
        device, size, used, available, percent, mountpoint = outdat.split("\n")[1].split()
        availableGB=atof(available)/(1024*1024)
        if availableGB > 15 :
            self.writeLog("INFO: Having enough space",0)
        else:
            self.writeLog("ERROR: Not having 150GB space; Terminating!",1)
            raise Exception("Insufficient storage")

    def createFolders(self):
        """Step 1. Create outdir and outdir/download"""
        #TODO use native python calls -SB
        makedir=call(["mkdir",self.outdir])
        if makedir:
            self.writeLog("ERROR: Can't create %s"%(self.outdir),1)
            raise Exception("Can't create %s"%(self.outdir))
        else:
            mkdir=call(["mkdir","%s/download"%(self.outdir)])
            if mkdir:
                #TODO use self.downloadFolder
                self.writeLog("ERROR: Can't create %s/download"%(self.outdir),1)
                raise Exception("Can't create %s/download"%(self.outdir))
            self.downloadFolder="%s/download"%(self.outdir)

    def downloadUniprot(self):
        """Step 2. Download the Uniprot XML file to downloadFolder"""
        self.writeLog("INFO: Uniprot download started",0)
        uniprotDownload=call(["wget","-q",self.urlUniref100xml,"-P",self.downloadFolder])
        if uniprotDownload:
            self.writeLog("ERROR: Can't download uniref100.xml.gz from %s"%(self.urlUniref100xml),2)
            raise Exception("Can't download uniref100.xml.gz from %s"%(self.urlUniref100xml))
        else:
            self.writeLog("INFO: Uniprot download finished",0)

    def downloadTaxonomy(self):
        """Step 3. Download taxonomy file to downloadFolder"""
        self.writeLog("INFO: Taxonomy download started",0)
        taxonomyDownload=call(["wget","-q",self.urlTaxonomy,"-O","%s/taxonomy-all.tab.gz"%(self.downloadFolder)])
        if taxonomyDownload:
            self.writeLog("ERROR: Can't download taxonomy-all.tab.gz from %s"%(self.urlTaxonomy),3)
            raise Exception("Can't download taxonomy-all.tab.gz from %s"%(self.urlTaxonomy))
        else:
            self.writeLog("INFO: Taxonomy download finished",0)

    def downloadSifts(self):
        """Step 4. Download the SIFTS pdb:uniprot mapping"""
        self.writeLog("INFO: SIFTS mapping file download started",0)
        #print "INFO: SIFTS mapping file download started"
        siftsDownload=call(["wget","-q",self.urlSifts,"-P",self.downloadFolder])
        if siftsDownload:
            self.writeLog("ERROR: Can't download SIFTS mapping file from %s"%(self.urlSifts),4)
            raise Exception("Can't download SIFTS mapping file from %s"%(self.urlSifts))
        else:
            self.writeLog("INFO: SIFTS mapping file download finished",0)

    def unzipTaxonomy(self):
        """Step 5. Unzip the taxonomy file"""
        self.writeLog("INFO: unzipping taxonomy files",0)
        unzipTaxonomy=call(["gunzip","%s/taxonomy-all.tab.gz"%(self.downloadFolder)])
        if unzipTaxonomy:
            self.writeLog("ERROR: Can't unzip taxonomy-all.tab.gz",5)
            raise Exception("Can't unzip taxonomy-all.tab.gz")
        else:
            self.writeLog("INFO: unzipping taxonomy files finished",0)

    def parseUniprotXml(self):
        """Step 6. Parse the uniprot XML file into tab-delimited format"""
        self.writeLog("INFO: Creating UniProt tab files started",0)
        parseuniprot=call(["java","-cp",self.eppicjar,"owl.core.connections.UnirefXMLParser","%s/uniref100.xml.gz"%(self.downloadFolder),\
                          "%s/uniref100.tab"%(self.downloadFolder),"%s/uniref100.clustermembers.tab"%(self.downloadFolder)])
        if parseuniprot:
            self.writeLog("ERROR: Can't create UniProt tab files;may be eppic.jar missing/too old (%s)"%self.eppicjar,6)
            raise Exception("Can't create UniProt tab files;may be eppic.jar missing/too old (%s)"%self.eppicjar)
        else:
            self.writeLog("INFO: Creating UniProt tab files finished",0)

    def createUniprotTables(self):
        """Step 7. Create Uniprot tables in the database"""
        self.writeLog("INFO: Creating UniProt tables started",0)
        for name, ddl in self.TABLES.iteritems():
            try:
                self.cursor.execute(ddl)
            except :
                self.writeLog("ERROR: Can't create table %s in %s"%(name, self.uniprotDatabase),7)
                raise Exception()
            self.writeLog("INFO: Table %s created"%(name),0)

    def uploadUniprotTable(self):
        """Step 8. Populate the uniprot database table from the parsed data"""
        self.writeLog("INFO: Uploading data into uniprot table in %s started"%(self.uniprotDatabase),0)
        sqlcmd='''LOAD DATA LOCAL INFILE '%s/uniref100.tab' INTO TABLE uniprot'''%(self.downloadFolder)
        try:
            self.cursor.execute(sqlcmd)
        except MySQLdb.Error, e:
            self.writeLog("ERROR: Can't upload data into uniprot table",8)
            try:
                self.writeLog("ERROR: MySQL Error [%d]: %s" % (e.args[0], e.args[1]),8)
                raise Exception()
            except IndexError:
                self.writeLog("ERROR: MySQL Error: %s" % str(e),8)
                raise Exception()
        self.writeLog("INFO: Uploading uniprot table finished",0)

    def uploadUniprotClustersTable(self):
        """Step 9. Populate the uniprot_clusters database table"""
        self.writeLog("INFO: Uploading data into uniprot_clusters in %s"%(self.uniprotDatabase),0)
        sqlcmd='''LOAD DATA LOCAL INFILE '%s/uniref100.clustermembers.tab' INTO TABLE uniprot_clusters'''%(self.downloadFolder)
        try:
            self.cursor.execute(sqlcmd)
        except MySQLdb.Error, e:
            self.writeLog("ERROR: Can't upload uniprot_cluster data",9)
            try:
                self.writeLog("ERROR: MySQL Error [%d]: %s" % (e.args[0], e.args[1]),9)
                raise Exception()
            except IndexError:
                self.writeLog("ERROR: MySQL Error: %s" % str(e),9)
                raise Exception()
        self.writeLog("INFO: Uploading uniprot_clusters finished",0)

    def uploadTaxonomyTable(self):
        """Step 10. Populate the taxonomy database table"""
        self.writeLog("INFO: Uploading data into taxonomy table in %s"%(self.uniprotDatabase),0)
        sqlcmd='''LOAD DATA LOCAL INFILE '%s/taxonomy-all.tab' INTO TABLE taxonomy IGNORE 1 LINES'''%(self.downloadFolder)
        try:
            self.cursor.execute(sqlcmd)
        except MySQLdb.Error, e:
            self.writeLog("ERROR: Can't upload taxonomy data",10)
            try:
                self.writeLog("ERROR: MySQL Error [%d]: %s" % (e.args[0], e.args[1]),10)
                raise Exception()
            except IndexError:
                self.writeLog("ERROR: MySQL Error: %s" % str(e),10)
                raise Exception()
        self.writeLog("INFO: Uploading taxonomy finished",0)


    def createUniprotIndex(self):
        """Step 11. Create database index for uniprot table"""
        self.writeLog("INFO: Indexing uniprot table started",0)
        sqlcmd="CREATE INDEX UNIPROTID_IDX ON uniprot (uniprot_id)"
        try:
            self.cursor.execute(sqlcmd)
        except MySQLdb.Error, e:
            self.writeLog("ERROR: Can't index uniprot table",11)
            try:
                self.writeLog("ERROR: MySQL Error [%d]: %s" % (e.args[0], e.args[1]),11)
                raise Exception()
            except IndexError:
                self.writeLog("ERROR: MySQL Error: %s" % str(e),11)
                raise Exception()
        self.writeLog("INFO: Indexing uniprot table finished",0)

    def downloadUniprotReldate(self):
        """Step 12. Download the release date"""
        self.writeLog("INFO: UniProt reldate download started",0)
        uniprotDownload=call(["wget","-q",self.urlUniprotReldate ,"-P",self.downloadFolder])
        if uniprotDownload:
            self.writeLog("ERROR: Can't download UniProt reldate from %s"%(self.urlUniprotReldate),12)
            raise Exception("Can't download UniProt reldate from %s"%(self.urlUniprotReldate))
        else:
            self.writeLog("INFO: UniProt reldate file download finished",0)
            #print "INFO: UniProt reldate file download finished"

    def downloadUniprotFasta(self):
        """Step 13. Download the Uniprot Fasta file to downloadFolder"""
        self.writeLog("INFO: UniProt FASTA file download started",0)
        uniprotDownload=call(["wget","-q",self.urlUniref100fasta,"-P",self.downloadFolder])
        if uniprotDownload:
            self.writeLog("ERROR: Can't download uniref100.fasta.gz from %s"%(self.urlUniref100fasta),13)
            raise Exception("Can't download uniref100.fasta.gz from %s"%(self.urlUniref100fasta))
        else:
            self.writeLog("INFO: UniProt FASTA file download finished",0)

    def createUniprotFiles(self):
        """Step 14. Expand the fasta files into uniprotDir and run `makeblastdb` to create the BLAST target database"""
        self.writeLog("INFO: Creating UniProt files started",0)
        makedir=call(["mkdir",self.uniprotDir])
        if makedir:
            self.writeLog("ERROR: Can't create %s"%(self.uniprotDir),14)
            raise Exception()
        else:
            mvfile=call(["mv","%s/uniref100.fasta.gz"%(self.downloadFolder),"%s/"%(self.uniprotDir)])
            if mvfile:
                self.writeLog("ERROR: Can't move %s/uniref100.fasta.gz"%(self.downloadFolder),14)
                raise Exception()
            else:
                makeblast=getstatusoutput("cd %s;gunzip -c uniref100.fasta.gz | makeblastdb -dbtype prot -logfile makeblastdb.log -parse_seqids -out uniref100.fasta -title uniref100.fasta"%(self.uniprotDir))
                if makeblast[0]:
                    self.writeLog("ERROR: Problem in running makeblast %s"%(makeblast[1]),14)
                    raise Exception()
                else:
                    cpreldate=getstatusoutput("cp %s/reldate.txt %s/"%(self.downloadFolder,self.uniprotDir))
                    if cpreldate[0]:
                        self.writeLog("ERROR: Can't copy reldate.txt file to uniprot folder %s"%(cpreldate[1]),14)
                        raise Exception()
                    else:
                        self.writeLog("INFO: UniProt files created",0)

    def createUniqueFasta(self):
        """Step 15. Create list of unique uniprot IDs and split into batches of 30'000."""
        self.writeLog("INFO: Creating unique fasta sequences",0)
        makedir=call(["mkdir",self.fastaFolder])
        if makedir:
            self.writeLog("ERROR: Can't create %s"%(self.fastaFolder),15)
            raise Exception()
        else:
            #TODO wrong way to do STDOUT redirection -SB
            uniquefasta=call(["java","-Xmx512m","-cp",self.eppicjar,"eppic.tools.WriteUniqueUniprots","-s",\
                              "%s/pdb_chain_uniprot.lst"%(self.downloadFolder),"-u",self.uniprotDatabase,"-o",\
                              "%s/"%(self.fastaFolder),">","%s/write-fasta.log"%(self.fastaFolder)])
            if uniquefasta:
                self.writeLog("ERROR: Creating unique sequences failed",15)
                raise Exception()
            else:
                splitqueries=call(["split","-l","30000","%s/queries.list"%(self.fastaFolder),"queries_"])
                mvfiels=getstatusoutput("mv queries_* %s/"%(self.fastaFolder))
                if mvfiels[0] or splitqueries:
                    self.writeLog("ERROR: Can't split queries",15)
                else:
                    self.writeLog("INFO: Unique fasta sequences created",0)


    def prepareFileTransfer(self):
        """Step 16. Consolidate files in clusterFolder"""
        self.writeLog("INFO: Preparing for file transfer",0)
        mkcdir=getstatusoutput("mkdir %s"%(self.clusterFolder))
        mvuniprot=call(["mv",self.uniprotDir,"%s/"%(self.clusterFolder)])
        if mkcdir[0]:
            self.writeLog("ERROR: Cant create %s"%(self.clusterFolder), 16)
            raise Exception()
        if mvuniprot:
            self.writeLog("ERROR: Can't move %s to %s/"%(self.uniprotDir,self.clusterFolder),16)
            raise Exception()
        else:
            mvfasta=call(["mv",self.fastaFolder,"%s/"%(self.clusterFolder)])
            if mvfasta:
                self.writeLog("ERROR: Can't move %s to %s/"%(self.fastaFolder,self.clusterFolder),16)
                raise Exception()
            else:
                self.writeLog("INFO: Prepared files for the cluster",0)
                self.writeLog("INFO : Please transfer %s to merlin"%(self.clusterFolder),0)
                self.writeLog("HINT: Command for file transfer")
                self.writeLog("HINT: rsync -avz %s <username>@merlinl01.psi.ch:"%(self.clusterFolder),0)
                self.writeLog("INFO: End of local calculation",0)

    def transferFiles(self):
        """Step 17. Rsync output to remote host"""
        self.writeLog("INFO: Transfering files to Merlin cluster",0)
        tfile=call(["rsync","az",self.clusterFolder,"%s@%s:%s"%(self.userName, self.remoteHost, self.remoteDir)])
        if tfile:
            self.writeLog("ERROR: Can't transfer files",17)
            raise Exception()
        else:
            self.writeLog("INFO: File transfer finished",17)

    def currentVersion(self):
        """Get the most recent uniprot Version"""
        if not hasattr(self,"_version"):
            self._version = urlopen(self.urlUniprotReldate).read().split("\n")[0].split(" ")[3]
        return self._version

    def runAll(self,checkpoint=0):
        """Run all steps sequentially.

        When errors occur, they print a checkpoint number in the log file.
        This can be used to resume the script after fixing the error.

        Arguments:
            checkpoint (int): Step number to resume at
        """

        if checkpoint < 1 or 17 < checkpoint:
            ValueError("Check point not in the list: Do manual debugging")

        if checkpoint <= 1:
            self.writeLog("INFO: EPPIC calculation started",0)
            self.checkMemory()
            self.connectDatabase()
            self.createFolders()
        else:
            self.writeLog("INFO: Resuming calculation from step %d"%checkpoint)
        if checkpoint <= 2:
            self.downloadUniprot() #download uniref100.xml.gz
        if checkpoint <= 3:
            self.downloadTaxonomy() # download taxonomy zip file
        if checkpoint <= 4:
            self.downloadSifts() # download Sifts mapping file
        if checkpoint <= 5:
            self.unzipTaxonomy() # unzipping taxonomy file
        if checkpoint <= 6:
            self.parseUniprotXml() # parse uniref100.xml.gz using eppic.jar to create .tab files for uploading into database
        if checkpoint <= 7:
            self.createUniprotTables() #create uniprot mysql table
        if checkpoint <= 8:
            self.uploadUniprotTable() # upload uniprot data into mysql table
        if checkpoint <= 9:
            self.uploadUniprotClustersTable() # upload uniprot_clusters data into mysql table
        if checkpoint <= 10:
            self.uploadTaxonomyTable() #upload taxonomy table
        if checkpoint <= 11:
            self.createUniprotIndex() # index the uniprot mysql table
        if checkpoint <= 12:
            self.downloadUniprotReldate() # download reldate.txt file
        if checkpoint <= 13:
            self.downloadUniprotFasta()# download uniprot fast file
        if checkpoint <= 14:
            self.createUniprotFiles()# parse and split the uniprot fast file
        if checkpoint <= 15:
            self.createUniqueFasta()# prepare unique sequence list for blast
        if checkpoint <= 16:
            self.prepareFileTransfer()# prepare files for merlin
        if checkpoint <= 17:
            self.transferFiles() # If you have passwd-free access to merlin then you can automaticallly transfer files


if __name__=="__main__":
    if len(sys.argv)==2:
        workdir=sys.argv[1]
        p=UniprotUpload(workdir)
        p.runAll()
    else:
        print "Usage: python %s <path to working dir>"%(sys.argv[0])

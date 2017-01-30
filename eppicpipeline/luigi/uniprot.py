import luigi
from luigi import Task,Parameter,BoolParameter,LocalTarget
from eppic_config import EppicConfig
import subprocess
from luigi.util import inherits,requires
import logging
import os
import eppicpipeline
from eppicpipeline.pipeline.UniprotUpload import UniprotUpload
from eppicpipeline.luigi.util import IncompleteException
import tempfile
from urllib2 import urlopen
import shutil

logger = logging.getLogger('luigi-interface')

class UniprotUploadTask(Task):
    """
    Download uniprot and prepare the uniprot database
    """
    #TODO default to the latest, and somehow pass the version to upstream tasks
    db = Parameter(description="Uniprot db date (e.g. 2017_01)", default=EppicConfig().db)
    allow_old = BoolParameter(description="Don't fail if the provided version is not the latest")

    uniprot_dir = Parameter(description="uniprot download directory",default=EppicConfig().uniprot_dir)
    jar = luigi.Parameter(default=EppicConfig().eppic_cli_jar)
    uniprot_db = Parameter(default=EppicConfig().uniprot_db)

    mysql_host = Parameter(default="localhost")
    mysql_user = Parameter(default=EppicConfig().db_root_user)
    mysql_password = Parameter(default=EppicConfig().db_root_password)

    dont_remove_tmp_dir=BoolParameter(description="In the case of errors, keep the temp directory around")
    ## Definitions for database downloads
    urlSifts = Parameter(description="sifts URL",
            default="ftp://ftp.ebi.ac.uk/pub/databases/msd/sifts/text/pdb_chain_uniprot.lst") #main ftp
    #urlSifts="ftp://ftp.uniprot.org/pub/databases/msd/sifts/text/pdb_chain_uniprot.lst" #UK mirror

    urlUniref100xml = Parameter(description="UniRef100 URL",
            default="ftp://ftp.expasy.org/databases/uniprot/current_release/uniref/uniref100/uniref100.xml.gz") #SWISS mirror
    #urlUniref100xml="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/uniref/uniref100/uniref100.xml.gz" #main ftp but slow

    urlUniprotReldate = Parameter(description="Uniprot version URL",
            default="ftp://ftp.expasy.org/databases/uniprot/current_release/knowledgebase/complete/reldate.txt") #Swiss mirror
    #urlUniprotReldate="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/reldate.txt" # main ftp

    urlUniref100fasta = Parameter(description="UniRef100 FASTA",
            default="ftp://ftp.expasy.org/databases/uniprot/current_release/uniref/uniref100/uniref100.fasta.gz") #Swiss mirror
    #urlUniref100fasta="ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/uniref/uniref100/uniref100.fasta.gz" #main ftp

    urlBlastdb = Parameter(description="Blast database URL",
            default="ftp://ftp.uniprot.org/pub") # main ftp
    #urlBlastdb="ftp://ftp.ebi.ac.uk/pub" # UK mirror

    urlTaxonomy="http://www.uniprot.org/taxonomy/?query=*&compress=yes&format=tab"


    def output(self):
        return {
            "uniprot_dir": LocalTarget(self.uniprot_dir),
        }
    def run(self):

        # Check that the input version is the latest
        if not self.allow_old and self.db != self.currentUniprot():
            raise IncompleteException("Uniprot database is out of date. Override with --allow-old")

        #mkdir /data/pipeline/eppic_${DATABASE_DATE}
        #python /usr/local/bin/UniprotUpload.py /data/pipeline/eppic_${DATABASE_DATE}
        outs = self.output()
        uniprot_dir = outs["uniprot_dir"]

        #Validate Parameters
        if not self.mysql_user:
            raise ValueError("No Mysql User")
        if not self.mysql_password:
            raise ValueError("No Mysql Password")
        if not self.mysql_host:
            raise ValueError("No Mysql Host")
        if not uniprot_dir:
            raise ValueError("No uniprot_dir")

        logger.info("mysql -h %s -u %s"%(self.mysql_host,self.mysql_user))

        #Use temporary directory
        #with uniprot_dir.temporary_path() as temp_path:
        temp_path = tempfile.mkdtemp(prefix="UniprotUploadTask_",dir=os.path.dirname(self.uniprot_dir))
        try:
            logger.info("Using temp dir %s instead of %s"%(temp_path,self.uniprot_dir))

            p = UniprotUpload( temp_path )
            # TODO finish parameterizing the UniprotUpload settings
            p.eppicjar = self.jar
            p.uniprotDatabase = self.uniprot_db
            p.mysqluser = self.mysql_user
            p.mysqlhost = self.mysql_host
            p.mysqlpasswd = self.mysql_password
            p.runAll()

            # Move results into correct destination
            shutil.move(temp_path,self.uniprot_dir)
        finally:
            # clean up temp_path if errors occured
            if not self.dont_remove_tmp_dir and os.path.exists(temp_path):
                logger.info("Removing temp dir %s",temp_path)
                shutil.rmtree(temp_path)
        # Check for completion
        if not self.complete():
            raise IncompleteException("Some files failed to generate: %s" % " ".join(f.path for _,f in outs.items() if not f.exists()))


    def currentUniprot(self):
        """Get the most recent uniprot Version"""
        return urlopen(self.urlUniprotReldate).read().split("\n")[0].split(" ")[3]

@requires(UniprotUploadTask)
class Main(Task):
    pass
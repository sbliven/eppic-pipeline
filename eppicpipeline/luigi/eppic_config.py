import luigi
from luigi import Parameter
import os.path

# Search for credentials in same places as luigi.cfg
from luigi.configuration import LuigiConfigParser
for path in LuigiConfigParser._config_paths:
    base = os.path.basename(path)
    if base == "luigi.cfg":
        d = os.path.dirname(path)
        LuigiConfigParser.add_config_path(os.path.join(d,"credentials.cfg"))

def eppicconfig():
    """Shorthand for EppicConfig.instance()"""
    return EppicConfig.instance()

def expandeppicvars(var):
    """Helper function to perform variable expansion using the EppicConfig context"""
    return var.format(**EppicConfig.instance().__dict__)

class EppicConfig(luigi.Config):
    """Global EPPIC configuration parameters

    Task-specific parameters may still be stored in their respective sections.
    However, parameters common to several tasks can use the global config section
    like this:

    `param = Parameter(default=eppiccli().param)`

    Using the instance() method to fetch the singleton is preferred over
    creating instances directly.

    All parameters undergo variable expansion. The str.format syntax is used
    (`param1 = derivation_of_{param2}`)
    """

    # Master run variable, used for generating other paths
    # Generally shouldn't be used directly by Tasks
    db = Parameter(description="Database date, e.g. 2016_01")
    # Specific database names
    eppic_db = Parameter(description="Eppic database name",
        default="eppic3_{db}")
    uniprot_db = Parameter(description="Uniprot database name",
        default="uniprot_{db}")
    mysql_host= Parameter(description="MySQL hostname",default="localhost")

    wui_files = Parameter(description="EPPIC output files")

    uniprot_dir = Parameter(description="uniprot download directory",default="")
    scratch_dir = Parameter(description="scratch directory (large temporary storage for compute nodes)",default="")

    sentinel_dir = Parameter(description="Directory for sentinel files. May be emptied between runs with impunity.",
        default="/tmp/luigi_sentinels")

    eppic_cli_conf_file = Parameter(description="Location for the eppic config file",
            default="./eppic_cli_{db}.conf")

    # Either specify eppic_source_dir and eppic_version,
    # or else give full paths to all jars
    eppic_source_dir = Parameter(description="Eppic source directory",default=".")
    eppic_version = Parameter(description="Eppic jar version",
        default="3.0-SNAPSHOT")
    eppic_cli_jar = Parameter(description="Location of the EPPIC CLI jar",
        default="{eppic_source_dir}/eppic-cli/target/uber-eppic-cli-{eppic_version}.jar")
    eppic_db_jar = Parameter(description="Location of the EPPIC dbtools jar",
        default="{eppic_source_dir}/eppic-dbtools/target/uber-eppic-dbtools-{eppic_version}.jar")

    blast_db_dir = Parameter(description="Path to Blast results")
    blast_cache_dir = Parameter(description="Path to Blast cache")
    local_cif_dir = Parameter(description="Local PDB file storage",
        default="")
    sifts_file = Parameter(description="Path to SIFTS file",
        default="{blast_db_dir}/pdb_chain_uniprot.lst")

    java = Parameter(description="Java 8 VM",default="java")
    blastclust = Parameter(description="BLASTCLUST executable")
    blast_data = Parameter(description="BLAST data files")
    blastp = Parameter(description="BLASTP executable")
    clustalo = Parameter(description="CLUSTALO executable")
    pymol = Parameter(description="PyMol executable")
    graphviz = Parameter(description="Graphviz (dot) executable")


    ## credentials.cfg
    ## NEVER USE THESE AS TASK PARAMETERS
    mysql_user= Parameter(description="MySQL user for standard actions",default="",significant=False)
    mysql_password= Parameter(description="MySQL password for standard actions",default="",significant=False)
    # MySQL user with create database permissions
    mysql_root_user= Parameter(description="MySQL user for database creation",default="",significant=False)
    mysql_root_password= Parameter(description="MySQL password for database creation",default="",significant=False)

    _instance = None
    @classmethod
    def instance(cls,*args,**kwargs):
        if cls._instance is None:
            cls._instance = cls(*args,**kwargs)
        return cls._instance

    def __getattribute__(self,name):
        # Any string attributes (e.g. Parameters) get passed through format
        # This expands singly-bracketed variables
        value = super(EppicConfig, self).__getattribute__(name)
        if hasattr(value, "format"):
            newvalue = value.format(**self.__dict__)
            while newvalue != value:
                value = newvalue
                newvalue = value.format(**self.__dict__)
        return value

    def get(self,key,default=None):
        # Make the config dict-like for use with handlebars
        try:
            return getattr(self,key)
        except AttributeError:
            return default

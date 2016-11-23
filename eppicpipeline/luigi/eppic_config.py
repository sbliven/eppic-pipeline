import luigi
from luigi import Parameter

import luigi.configuration
luigi.configuration.LuigiConfigParser.add_config_path("config/credentials.cfg")
luigi.configuration.LuigiConfigParser.add_config_path("config/luigi.cfg")

class EppicConfig(luigi.Config):
    # Master run variable, used for generating other paths
    # Generally shouldn't be used directly by Tasks
    db = Parameter(description="Database date, e.g. 2016_01")
    # Specific database names
    eppic_db = Parameter(description="Eppic database name",
        default="eppic3_{db}")
    uniprot_db = Parameter(description="Uniprot database name",
        default="uniprot_{db}")

    eppic_source_dir = Parameter(description="Eppic source directory")
    wui_files = Parameter(description="EPPIC output files")

    eppic_version = Parameter(description="Eppic jar version",
        default="3.0-SNAPSHOT")
    eppic_cli_jar = Parameter(description="Location of the EPPIC CLI jar",
        default="{eppic_source}/eppic-cli/target/uber-eppic-cli-{eppic_version}.jar")
    eppic_db_jar = Parameter(description="Location of the EPPIC dbtools jar",
        default="{eppic_source}/eppic-dbtools/target/uber-eppic-dbtools-{eppic_version}.jar")

    blast_db_dir = Parameter(description="Path to Blast results")
    blast_cache_dir = Parameter(description="Path to Blast cache")
    local_cif_dir = Parameter(description="Local PDB file storage",
        default=None)
    sifts_file = Parameter(description="Path to SIFT file",
        default="{blast_db_dir}/pdb_chain_uniprot.lst")

    blastclust = Parameter(description="BLASTCLUST executable")
    blast_data = Parameter(description="BLAST data files")
    blastp = Parameter(description="BLASTP executable")
    clustalo = Parameter(description="CLUSTALO executable")
    pymol = Parameter(description="PyMol executable")
    graphviz = Parameter(description="Graphviz (dot) executable")

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

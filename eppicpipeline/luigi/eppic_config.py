import luigi

import luigi.configuration
luigi.configuration.LuigiConfigParser.add_config_path("credentials.cfg")

class EppicConfig(luigi.Config):
    # Master run variable, used for generating other paths
    # Generally shouldn't be used directly by Tasks
    run_date = luigi.Parameter(description="Database date, e.g. 2016_01")
    # Specific database names
    eppic_db = luigi.Parameter(default="eppic3_{}_test".format(run_date),
            description="Eppic database name")
    uniprot_db = luigi.Parameter(default="uniprot_{}".format(run_date),
            description="Uniprot database name")

    eppic_source_dir = luigi.Parameter(description="Path to eppic source directory")
    eppic_version = luigi.Parameter(default="3.0-SNAPSHOT",
            description="Eppic version")


# eppic-pipeline

# Installation

The EPPIC pipeline is composed primarily of a python package. This can be installed easily using the setup script. For development, it is recommended to install into a [virtualenv](https://pypi.python.org/pypi/virtualenv) environment to isolate any dependencies and reduce the need for root permissions. On the dev server this environment is activated with the command `workon luigi`, while the merlin cluster uses a slightly different command (see below).

Several important additions have been added to luigi. First, install luigi from the _eppic-team_ fork. Then, the eppicpipeline package can be installed in the usual way.

```
pip install https://github.com/eppic-team/luigi/archive/master.zip

python setup.py install
```

This command should install all dependencies from pypi. There are a few issues with scientific linux. The python_daemon package didn't compile for me, so it was compiled on an ubuntu machine and installed from the wheel (.whl) file.

# Workflow overview

The goal of the project is to combine steps as much as possible, so that the workflow can be run on a clean system with minimal requirements. However, for efficient computation and I/O the normal pipline is split into several steps to be run on their respective servers:

1. **Uniprot database initialization** Run on the database host to populate the uniprot_db and associated files. Run monthly on the db host.
2. (Optional) **Blast precomputation** Blast can be run for all uniprot entries to reduce later calculation time for redundant structures.
3. **EPPIC calculation** Run EPPIC CLI over new jobs. Can be run locally for development (`EppicCli` or `EppicList`), or on an SGE cluster (`SGEEppicList`). Run weekly on the cluster.
4. **WUI setup** Uploads CLI jobs to eppic_db and configures jetty for serving the files. Run on the web server.

Configuration is explained below in detail. After configuration, the following commands should control the full process:

1. From the db host:
```
# Download uniprot
luigi --module eppicpipeline.luigi.uniprot Main
```

2. From the SGE cluster:
```
luigi --module eppicpipeline.luigi.sge_pipeline Main
```

3. From the web server:
```
luigi --module eppicpipeline.luigi.wui Main
```


# Uniprot download

Typically kicked off with
```
# Download uniprot
luigi --module eppicpipeline.luigi.uniprot Main
```

Currently this downloads everything and also transfers the output files to the SGE cluster. It requires password-less rsync. At a minimum, set the following parameters:
```
[UniprotUploadTask]
remote_host=<sge host>
remot_user=<username>
```

If something goes wrong and you have `dont_remove_tmp_dir=True`, it is possible to resume the task midway. Depending on the error, this could lead to database corruption, so make sure you understand the steps in `eppicpipeline.pipeline.UniprotUpload`.
```
luigi --module eppicpipeline.luigi.uniprot UniprotUploadTask --dont-remove-tmp-dir --resume-dir=<temporary dir> --resume-step=<resume step> --overwrite-behavior=IGNORE
```

Many downstream tasks rely on `UniprotUploadStub`, which throws an error if the `UniprotUploadTask` hasn't previously been run or it's outputs haven't been copied to the current host.


# Running the CLI on an SGE cluster (e.g. Merlin)

On merlin, the easiest way to install all dependencies is to use a conda virtual environment.

~/.bashrc:
```{bash}
# load the conda module
test -e /opt/psi/config/profile.bash && source /opt/psi/config/profile.bash
module load psi-python27/2.3.0

# Cache directories
mkdir -p /scratch/bliven_s/pdb
export ATOM_CACHE_DIR=/scratch/bliven_s/pdb
export PDB_DIR=/scratch/bliven_s/pdb
export PDB_CACHE_DIR=/scratch/bliven_s/pdb

# Compute nodes may not find the default luigi.cfg
export LUIGI_CONFIG_PATH=$HOME/eppic-pipeline/config/luigi.cfg
```

On a new system, next set up the conda environment (here called 'luigi'):

```
conda create --name luigi ipython
```

To enable this, call `source activate luigi`. This allows dependencies to be installed into an isolated python environment.

Note that this command needs to be run on compute nodes. This can be done either by setting it in your .bashrc file, or by setting the job_format variable for SGEEppicCli and other CustomSGEJobTask instances:
```
# in luigi.cfg
job_format = source activate luigi && python {0} "{1}" "{2}"
```


Copy `config/luigi.cfg.example` to `$LUIGI_CONFIG_PATH` and customize all options.


To run the CLI on a list of PDB IDs, use the following command:

```
luigi --module eppicpipeline.luigi.eppic_cli SGEEppicList --input-list=$HOME/pdbs.list
```

To run locally, use the `EppicList` task instead.

## Cleaning up

After running, an easy way to wipe the scratch dirs is to sync an empty blast_database directory:

```
mkdir /tmp/blast_database
luigi --module eppicpipeline.luigi.sge_pipeline ScratchDistributor --seed=`date +%s` --blast-db-dir=/tmp/blast_database/
```



# Known bugs

- `pipeline.UniprotUpload` should be a set of independent luigi tasks, rather than using the old resume system
- `UniprotUploadTask`'s `uniprot_dir` is different from `EppicCli`'s parameter of the same name.
- Store DB parameters securely
- Improve data transfer organization. I prefer "pull" transfers over "push", but we should at least be consistent.

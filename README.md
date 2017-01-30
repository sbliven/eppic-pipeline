# eppic-pipeline

# Installation

The EPPIC pipeline is composed primarily of a python package. This can be installed easily using the setup script. For development, it is recommended to install into a [virtualenv](https://pypi.python.org/pypi/virtualenv) environment to isolate any dependencies and reduce the need for root permissions. On the dev server this environment is activated with the command `workon luigi`, while the merlin cluster uses a slightly different command (see below).

```
python setup.py install
```

This command should install all dependencies from pypi. There are a few issues with scientific linux. The python_daemon package didn't compile for me, so it was compiled on an ubuntu machine and installed from the wheel (.whl) file.

# Downloading uniprot

```
luigi --module eppicpipeline.luigi.uniprot Main
```

# Running the CLI on an SGE cluster (e.g. Merlin)

On merlin, the easiest way to install all dependencies is to use a conda virtual environment.

~/.bashrc:
```{bash}
# load the conda module
test -e /opt/psi/config/profile.bash && source /opt/psi/config/profile.bash
module load psi-python27/2.3.0

# Cache directories
export ATOM_CACHE_DIR=/scratch/bliven_s/pdb
export PDB_DIR=/scratch/bliven_s/pdb
export PDB_CACHE_DIR=/scratch/bliven_s/pdb

# Compute nodes may not find the default luigi.cfg
export LUIGI_CONFIG_PATH=$HOME/eppic-pipeline/config/luigi.cfg
```

On a new system, next set up the condor environment (here called 'luigi'):

```
conda create --name luigi ipython
```

To enable this, call `source activate luigi`. This allows dependencies to be installed into an isolated python environment.

Note that this command needs to be run on compute nodes. This can be done either by setting it in your .bashrc file, or by setting the job_format variable for SGEEppicCli and other CustomSGEJobTask instances.

Copy `config/luigi.cfg.example` to `$LUIGI_CONFIG_PATH` and customize all options.


To run the CLI on a list of PDB IDs, use the following command:

```
luigi --module eppicpipeline.luigi.eppic_cli SGEEppicList --input-list=$HOME/pdbs.list
```

To run locally, use the `EppicList` task instead.


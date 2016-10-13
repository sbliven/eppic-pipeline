# eppic-pipeline

Main repository of scripts for running EPPIC 3, generally with the intent of
generating data for the web server.

EPPIC support the following use cases:
1. Local EPPIC database & server with minimal set of test cases
2. Pipeline to compute the full PDB
3. Topup pipeline to keep an existing installation up-to-date

# Organization

- *config* Configuration variables. Be careful about checking things in here
- *docker* Scripts for building docker images, if any
- *scripts* All scripts for running EPPIC
  - *local* Scripts for directly running EPPIC locally on a small set of jobs
  - *pipeline* Scripts for PDB-wide analysis. Depends on local scripts
    - *dev* Scripts that should be run on the dev server
    - *sge* Scripts intended to be run on a cluster running Sun Grid Engine
    - *web* Scripts to run on the production web server
  - *topup* Scripts for augmenting a PDB-wide analysis. Depends on local and pipeline scripts
  - *unmigrated* Raw scripts collected from various hosts. These are intended to be organized into the other folders over time.

# Configuration

All paths and external resources are configured through config/pipeline.conf.

Passwords are stored in config/credentials.conf, which can be copied from the example

# Workflows


# Misc notes

```
# sync merlin results back to local
rsync -av merlinl01:/gpfs/home/bliven_s/eppic-3.0/output/data  /data/spencer/eppic/wui/files3_2016_05_test
```


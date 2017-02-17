"""
Tasks relating to parallel, distributed computation on an SGE cluster
"""

import luigi
import os
import time
import logging
from pkg_resources import resource_string
from luigi import Task,WrapperTask,Parameter,ListParameter
from luigi.util import inherits,requires
from eppicpipeline.luigi.util import IncompleteException, ExternalFile, RemoteExternalFile, CachedRemoteFile, RsyncTask
from eppicpipeline.luigi.uniprot import UniprotUploadStub
from eppicpipeline.luigi.eppic_config import eppicconfig

logger = logging.getLogger('luigi-interface')


class ScratchDistributor(WrapperTask):
    hosts = ListParameter(description="List of destination hosts",default=[])
    hosts_file = Parameter(description="File with list of destination hosts",default="")
    scratch_dir = Parameter(description="Scratch directory on compute nodes",default=eppicconfig().scratch_dir)
    blast_db_dir = Parameter(description="Path to Blast results",default=eppicconfig().blast_db_dir)
    seed = Parameter(description="Unique seed to ensure the task runs")

    def requires(self):
        infile = None
        if self.hosts_file:
            infile = self.clone(ExternalFile,filename=self.hosts_file)
            yield infile

        yield self.clone(UniprotUploadStub,remote_host="localhost")

        # Generate task for each host
        hosts = list(self.hosts)

        # if no no hosts given, use internal file
        if not hosts and infile is None:
            logger.info("Using default hosts list")
            hosts_file = resource_string(__name__, 'hosts.list')
            hosts = [h.strip() for h in hosts_file.split() if h[0] != "#"]

        if infile is not None and infile.complete():
            with infile.output().open('r') as hostfile:
                for host in hostfile:
                    host = host.strip()
                    if host[0] != "#":
                        hosts.append(host)

        logger.info("Syncing scratch to %d hosts"%len(hosts))

        opts = "-avz --delete"
        # No trailing /
        src = os.path.dirname(os.path.join(self.blast_db_dir,""))
        # Add trailing /
        dst = os.path.join(self.scratch_dir,"")
        for host in hosts:
            yield RsyncTask(src=src,dst=dst,dst_host=host,seed=self.seed,opts=opts)


#@requires()
class Main(Task):
    pass

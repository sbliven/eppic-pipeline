from luigi import Task, WrapperTask, Parameter
from luigi.util import inherits,requires
import os

from eppicpipeline.luigi.database import SafeMySqlTarget
from eppicpipeline.luigi.eppic_config import eppicconfig,expandeppicvars
from eppicpipeline.luigi.eppic_cli import UploadEppicCli
from eppicpipeline.luigi.util import RsyncTask

class RsyncWuiFiles(WrapperTask):
    compute_host = Parameter(description="Host with eppic results")
    compute_user = Parameter(description="User for compute_host")
    compute_wui_files = Parameter(description="Location of wui_files on compute_host")
    wui_files = Parameter(description="Local EPPIC output files",default=eppicconfig().wui_files)
    seed = Parameter(description="Unique seed to ensure the task runs")
    opts = Parameter(description="options passed to rsync",default="-avz --delete")

    def requires(self):
        out = expandeppicvars(self.compute_wui_files)
        out = os.path.join(out,"") #Add trailing /
        reqs = {
            "rsync": RsyncTask(src_host=self.compute_host,
                               src_user=self.compute_user,
                               src=out,
                               dst=self.wui_files,
                               dst_host="", #localhost
                               seed=self.seed,
                               opts=self.opts,
                               )
        }
        return reqs

@inherits(UploadEppicCli)
class Wui(WrapperTask):
    def requires(self):
        #TODO how to force Rsync to run first?
        yield RsyncWuiFiles()
        # yield SafeMySqlTarget()
        yield self.clone(UploadEppicCli)

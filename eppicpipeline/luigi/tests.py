import time
import logging
from luigi import Task, WrapperTask, LocalTarget, Parameter
from luigi.util import inherits,requires

logger = logging.getLogger('luigi-interface')

class Test(Task):
    out = Parameter(description="output file")
    def output(self):
        return LocalTarget(self.out)
    def run(self):
        print("Running Test task. Outputting to %s"%self.out)
        with self.output().open('w') as o:
            o.write("Running Test task at %s\n"%time.time())

# Tests for running a task exactly once
# See https://groups.google.com/forum/#!searchin/luigi-user/always$20run%7Csort:relevance/luigi-user/p_CO1IVGCJU/QOYvoBmUTeMJ

class RunAlwaysFlag(Task):
    def __init__(self,*args,**kwargs):
        super(RunAlwaysFlag,self).__init__(*args,**kwargs)
        self.done=False
    def complete(self):
        return self.done
    def run(self):
        self.done = True
        logger.info( "Running %s"%(self))

@requires(RunAlwaysFlag)
class RunAlwaysFlagWrapper(WrapperTask):
    pass


class RunAlwaysSeeded(Task):
    seed = Parameter(description="unique seed (e.g. from `date '+%s'`)")
    # def complete(self):
    #     return False
    def run(self):
        logger.info( "Running %s"%(self))

#@requires(RunAlwaysSeeded)
class RunAlwaysSeededWrapper(WrapperTask):
    def requires(self):
        return RunAlwaysSeeded(seed=str(time.time()))


class RunAlwaysSentinel(Task):
    seed = Parameter(description="unique seed (e.g. from `date '+%s'`)")
    def output(self):
        return LocalTarget("sentinel_%s"%self.seed)
    def run(self):
        logger.info( "Running %s"%(self))
        with self.output().open('w') as out:
            pass

@requires(RunAlwaysSentinel)
class RunAlwaysSentinelWrapper(WrapperTask):
    pass

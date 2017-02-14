import luigi
from luigi import Task,Parameter, WrapperTask,ExternalTask,LocalTarget,BoolParameter
from eppicpipeline.luigi.eppic_config import eppicconfig
from pkg_resources import resource_string#, resource_stream, resource_listdir
import pybars as hb
import subprocess
from sgetask import CustomSGEJobTask
from luigi.util import inherits,requires
import logging
import os
from eppicpipeline.luigi.util import IncompleteException,ExternalFile
from eppicpipeline.luigi.uniprot import UniprotUploadStub

logger = logging.getLogger('luigi-interface')


class SiftsFile(Task):
    pass

class EppicCli(Task):
    #input; required
    pdb = Parameter(description="Input PDB ID")
    out = Parameter(default="{}/data/divided/{{mid2}}/{{pdb}}".format(
        eppicconfig().wui_files)
    )
    log = Parameter(default="") #Empty for no log
    jar = Parameter(default=eppicconfig().eppic_cli_jar)
    java = Parameter(default=eppicconfig().java)
    skip_entropy = BoolParameter(description="Don't calculate entropy scores",
                                 significant=True)

    mysql_host = Parameter(default=eppicconfig().mysql_host)
    mysql_user = Parameter(default=eppicconfig().mysql_root_user,significant=False)
    mysql_password = Parameter(default=eppicconfig().mysql_root_password,significant=False)

    def requires(self):
        reqs = {
                "conf":self.clone(CreateEppicConfig),
                "jar":self.clone(ExternalFile,filename=self.jar),
                }
        # Require uniprot database for entropies
        if not self.skip_entropy:
            # Stub fails if the db is missing rather than calculating it
            reqs["db"] = self.clone(UniprotUploadStub,remote_host="localhost")
        return reqs

    def outputdir(self):
        return str(self.out).format(mid2=self.pdb[1:3].lower(),pdb=self.pdb.lower())
    def output(self):
        outs = {
            "dir":LocalTarget(self.outputdir()),
            "finished":LocalTarget("{}/finished".format(self.outputdir()) )
            }
        if self.log:
            outs["log"]=LocalTarget(self.log)
        return outs

    def run(self):
        super(EppicCli,self).run()
        conf = self.requires()["conf"]
        outs = self.output()
        log = outs.get("log") #None if not set

        dirname = os.path.dirname(self.outputdir())
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as err:
                if not os.path.exists(dirname):
                    raise err
                else:
                    logger.warn("Concurrent creation of %s",dirname)

        cmd = [self.java,
            "-Xmx3g","-Xmn1g",
            "-jar",str(self.jar),
            "-i", str(self.pdb),
            "-o", str(self.outputdir()),
            "-a","1", #threads
            "-w", #webui.dat
            "-g",conf.eppic_cli_conf_file,
            "-l", #pymol images
            "-P", #assembly diagrams
            "-p", #interface coordinates
        ]
        if not self.skip_entropy:
            cmd.append("-s") #entropy scores

        rtn = -1
        if log is not None:
            with log.open('w') as out:
                out.write("CMD: %s\n"%" ".join(cmd))
                out.flush()
                rtn = subprocess.call(cmd,stdout=out,stderr=subprocess.STDOUT)
        else:
            rtn = subprocess.call(cmd)
        if rtn > 0:
            raise IncompleteException("Non-zero return value (%d) from %s"%(rtn," ".join(cmd)))
        if not self.complete():
            raise IncompleteException("Some outputs were not generated")


class CreateEppicConfig(Task):
    eppic_cli_conf_file = Parameter(default=eppicconfig().eppic_cli_conf_file)

    def output(self):
        return LocalTarget(self.eppic_cli_conf_file)

    def run(self):
        conf = resource_string(__name__, 'eppic.conf.hbs')
        compiler = hb.Compiler()
        # pybars seems to accept only strings (v0.0.4)
        template = compiler.compile(unicode(conf))
        confstr = template(eppicconfig())
        # Write to output
        with self.output().open('w') as out:
            if type(confstr) == hb.strlist:
                for s in confstr:
                    out.write(s)
            else:
                out.write(confstr)

@inherits(EppicCli)
class SGEEppicCli(CustomSGEJobTask):
    def requires(self):
        reqs = {
                "conf":self.clone(CreateEppicConfig),
                "jar":self.clone(ExternalFile,filename=self.jar),
                }
        # Require uniprot database for entropies
        if not self.skip_entropy:
            # Stub fails if the db is missing rather than calculating it
            reqs["db"] = self.clone(UniprotUploadStub,remote_host="localhost")
        return reqs

    def outputdir(self):
        return str(self.out).format(mid2=self.pdb[1:3].lower(),pdb=self.pdb.lower())
    def output(self):
        outs = {
            "dir":LocalTarget(self.outputdir()),
            "finished":LocalTarget("{}/finished".format(self.outputdir()) )
            }
        if self.log:
            outs["log"]=LocalTarget(self.log)
        return outs

    def work(self):
        conf = self.requires()["conf"]
        outs = self.output()
        log = outs.get("log") #None if not set

        dirname = os.path.dirname(self.outputdir())
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except OSError as err:
                if not os.path.exists(dirname):
                    raise err
                else:
                    logger.warn("Concurrent creation of %s",dirname)

        cmd = [self.java,
            "-Xmx3g","-Xmn1g",
            "-jar",str(self.jar),
            "-i", str(self.pdb),
            "-o", str(self.outputdir()),
            "-a","1", #threads
            "-w", #webui.dat
            "-g",conf.eppic_cli_conf_file,
            "-l", #pymol images
            "-P", #assembly diagrams
            "-p", #interface coordinates
        ]
        if not self.skip_entropy:
            cmd.append("-s") #entropy scores

        rtn = -1
        if log is not None:
            with log.open('w') as out:
                out.write("CMD: %s\n"%" ".join(cmd))
                out.flush()
                rtn = subprocess.call(cmd,stdout=out,stderr=subprocess.STDOUT)
        else:
            rtn = subprocess.call(cmd)
        if rtn > 0:
            raise IncompleteException("Non-zero return value (%d) from %s"%(rtn," ".join(cmd)))
        if not self.complete():
            raise IncompleteException("Some outputs were not generated")

class EppicList(WrapperTask):
    input_list = Parameter(description="File containing a list of PDB IDs to run")

    wui_files = Parameter(description="EPPIC output files root dir", default=eppicconfig().wui_files)

    def requires(self):
        # Require the input
        infile = self.clone(ExternalFile,filename=self.input_list)
        yield infile

        # Dynamically generate more requirements from the input
        if infile is not None and infile.complete():
            with infile.output().open('r') as inputs:
                #Each pdb should be a single line
                logger.debug("Calculating dependencies from %s"%self.input_list)
                deps =  [ self.makeTask(pdb.strip().lower())
                        for pdb in inputs
                        if pdb.strip() and pdb[0]!='#' ]
                for dep in deps:
                    logger.debug("Requiring %s"%dep)#(dep.__class__.__name__,dep.pdb if dep is not None else None))
                    yield dep

    def makeTask(self,pdb):
        logger.info("Creating EppicCli task for %s"%pdb)
        outputdir = os.path.join(self.wui_files, "data", "divided", pdb[1:3].lower(), pdb.lower())
        logfile = os.path.join(outputdir,pdb+".out")
        return self.clone(EppicCli, pdb=pdb, out=outputdir, log=logfile)

@inherits(EppicList)
class SGEEppicList(EppicList):
    def makeTask(self,pdb):
        outputdir = os.path.join(self.wui_files, "data", "divided", pdb[1:3].lower(), pdb.lower())
        logfile = os.path.join(outputdir,pdb+".out")
        return SGEEppicCli(pdb=pdb,
                    out=outputdir,
                    log=logfile)


@requires(SGEEppicList)
class Main(WrapperTask):
    pass

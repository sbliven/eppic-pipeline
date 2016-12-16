import luigi
import eppic_config
from pkg_resources import resource_string#, resource_stream, resource_listdir
import pybars as hb
import subprocess

config = eppic_config.EppicConfig()

class EppicCli(luigi.Task):
    #input; required
    pdb = luigi.Parameter()
    out = luigi.Parameter(default="{}/data/divided/{{mid2}}/{{pdb}}".format(
        config.wui_files)
    )
    log = luigi.Parameter(default=None)
    jar = luigi.Parameter(default="{}/eppic-cli/target/uber-eppic-cli-{}.jar".format(
        config.eppic_source_dir, config.eppic_version))

    def requires(self):
        return CreateEppicConfig()

    def outputdir(self):
        return str(self.out).format(mid2=self.pdb[1:3],pdb=self.pdb)
    def output(self):
        return {
            "log":luigi.LocalTarget(self.log) if self.log is not None else None,
            "dir":luigi.LocalTarget(self.outputdir()),
            "finished":luigi.LocalTarget("{}/finished".format(self.outputdir()) )
            }

    def run(self):
        conf = self.input()
        log = self.output()["log"]

        cmd = ["java",
            "-Xmx3g","-Xmn1g",
            "-jar",str(self.jar),
            "-i", str(self.pdb),
            "-o", str(self.outputdir()),
            "-a","1", #threads
            "-w", #webui.dat
            "-g",conf.open().name, #Is there a way to get the path without opening it?
            "-l", #pymol images
            #"-s", #entropy scores
            "-P", #assembly diagrams
            "-p", #interface coordinates
        ]
        if log is not None:
            with self.output()["log"].open('w') as out:
                out.write("CMD: "+" ".join(cmd))
                return subprocess.call(cmd,stdout=out,stderr=subprocess.STDOUT)
        else:
            return subprocess.call(cmd)


class CreateEppicConfig(luigi.Task):
    eppic_conf_file = luigi.Parameter(default="eppic_{}.conf".format(config.db))

    def output(self):
        return luigi.LocalTarget(self.eppic_conf_file)

    def run(self):
        conf = resource_string(__name__, 'eppic.conf.hbs')
        compiler = hb.Compiler()
        # pybars seems to accept only strings (v0.0.4)
        template = compiler.compile(unicode(conf))
        confstr = template(config)
        # Write to output
        with self.output().open('w') as out:
            if type(confstr) == hb.strlist:
                for s in confstr:
                    out.write(s)
            else:
                out.write(confstr)



class EppicCliTest(luigi.Task):
    jar = luigi.Parameter(default="{}/eppic-cli/target/uber-eppic-cli-{}.jar".format(config.eppic_source_dir, config.eppic_version))
    def run(self):
        print( "Jar={}\n".format(self.jar))

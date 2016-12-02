import luigi
import eppic_config
from pkg_resources import resource_string#, resource_stream, resource_listdir
import pybars as hb

config = eppic_config.EppicConfig()

class EppicCli(luigi.Task):
    jar = luigi.Parameter(default="{}/eppic-cli/target/uber-eppic-cli-{}.jar".format(config.eppic_source_dir, config.eppic_version))

    def requires(self):
        return CreateEppicConfig()

    def output(self):
        return luigi.LocalTarget("eppic_cli.out")

    def run(self):
        with self.output().open('w') as out:
            out.write("Jar={}\n".format(self.jar))

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

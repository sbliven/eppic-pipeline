import luigi
import eppic_config

config = eppic_config.EppicConfig()

class EppicCli(luigi.Task):
    jar = luigi.Parameter(default="{}/eppic-cli/target/uber-eppic-cli-{}.jar".format(config.eppic_source_dir, config.eppic_version))

    def output(self):
        return luigi.LocalTarget("eppic_cli.out")

    def run(self):
        with self.output().open('w') as out:
            out.write("Jar={}\n".format(self.jar))


class EppicCliTest(luigi.Task):
    jar = luigi.Parameter(default="{}/eppic-cli/target/uber-eppic-cli-{}.jar".format(config.eppic_source_dir, config.eppic_version))
    def run(self):
        print( "Jar={}\n".format(self.jar))

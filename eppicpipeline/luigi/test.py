import luigi
import eppic_config

class TestTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget("test.out")

    def run(self):
        with self.output().open('w') as out:
            out.write("testing")


# if __name__ == "__main__":
#     luigi.run()

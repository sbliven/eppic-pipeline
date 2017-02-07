import logging
import luigi
import os
from luigi.contrib.sge import SGEJobTask,LocalSGEJobTask
import subprocess
from luigi.contrib import sge_runner

logger = logging.getLogger('luigi-interface')

import eppicpipeline
luigi.contrib.sge.attach(eppicpipeline)

def _build_qsub_command(cmd, job_name, outfile, errfile, pe, n_cpu):
    """Submit shell command to SGE queue via `qsub`"""
    qsub_template = """echo "{cmd}" | qsub -o ":{outfile}" -e ":{errfile}" -V -r y -pe {pe} {n_cpu} -N {job_name}"""
    escaped_cmd = cmd.replace('"','\\"')
    return qsub_template.format(
        cmd=escaped_cmd, job_name=job_name, outfile=outfile, errfile=errfile,
        pe=pe, n_cpu=n_cpu)


class CustomSGEJobTask(SGEJobTask):
    """ Equivalent to SGEJobTask, but allows custom commands to be passed to qsub
    """
    job_format = luigi.Parameter(significant=False, default='python {0} "{1}" "{2}"',
            description="Command run by qsub. Formatted with the runner_path, the temp dir, and the current directory")

    def run(self):
        super(CustomSGEJobTask,self).run()
        print("--- CustomSGEJobTask.run ---")

    def _run_job(self):


        # Build a qsub argument that will run sge_runner.py on the directory we've specified
        runner_path = sge_runner.__file__
        if runner_path.endswith("pyc"):
            runner_path = runner_path[:-3] + "py"
        job_str = self.job_format.format(
            runner_path, self.tmp_dir, os.getcwd())  # enclose tmp_dir in quotes to protect from special escape chars
        if self.no_tarball:
            job_str += ' "--no-tarball"'

        # Build qsub submit command
        self.outfile = os.path.join(self.tmp_dir, 'job.out')
        self.errfile = os.path.join(self.tmp_dir, 'job.err')
        submit_cmd = _build_qsub_command(job_str, self.task_family, self.outfile,
                                         self.errfile, self.parallel_env, self.n_cpu)
        logger.debug('qsub command: \n' + submit_cmd)

        # Submit the job and grab job ID
        output = subprocess.check_output(submit_cmd, shell=True)
        self.job_id = luigi.contrib.sge._parse_qsub_job_id(output)
        logger.debug("Submitted job to qsub with response:\n" + output)

        self._track_job()

        # Now delete the temporaries, if they're there.
        if (self.tmp_dir and os.path.exists(self.tmp_dir) and not self.dont_remove_tmp_dir):
            logger.info('Removing temporary directory %s' % self.tmp_dir)
            subprocess.call(["rm", "-rf", self.tmp_dir])

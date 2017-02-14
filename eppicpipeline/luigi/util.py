import luigi
from luigi import Task,Parameter,LocalTarget,ExternalTask
import urllib2
import subprocess32
import logging
import os
import shlex
from luigi.contrib.ssh import RemoteTarget
from eppicpipeline.luigi.eppic_config import eppicconfig

logger = logging.getLogger('luigi-interface')

class IncompleteException(Exception):
    """General error for tasks that didn't completer"""
    pass

class ExternalFile(ExternalTask):
    filename = Parameter()
    def output(self):
        return LocalTarget(self.filename)

class RemoteExternalFile(ExternalTask):
    filename = Parameter()
    host = Parameter()

    def output(self):
        return RemoteTarget(self.filename,self.host)

class CachedRemoteFile(Task):
    """Download a remote file to a known local location"""
    filename = Parameter(description="Local path")
    url = Parameter(description="URL to download the file",significant=False)

    def output(self):
        return LocalTarget(self.filename)

    def run(self):
        logger.info("Downloading {url} to {filename}".format(**self.__dict__))
        response = urllib2.urlopen(self.url)
        chunksize = 1024
        with self.output().open('wb') as tmp:
            for chunk in iter(lambda: response.read(chunksize), ''):
                tmp.write(chunk)


class RsyncTask(Task):
    """
    Uses rsync to transfer directories between potentially remote destinations

    Note that this should only be used for initial transfers, as it will not
    be run if the destination directory exists.

    Also note that src should end with at / if it is a directory.
    """
    sentinel_dir = Parameter(description="Directory for sentinel files. May be emptied between runs with impunity.",
        default=eppicconfig().sentinel_dir)
    seed = Parameter(description="Unique seed to ensure the task runs")

    opts = Parameter(description="options passed to rsync",default="-avz")
    src = Parameter()
    dst = Parameter()
    src_host = Parameter(default="")
    src_user = Parameter(default="")
    dst_host = Parameter(default="")
    dst_user = Parameter(default="")

    def requires(self):
        if self.src_host:
            yield RemoteExternalFile(filename=self.src,host=self.src_host)
        else:
            yield ExternalFile(filename=self.src)

    def output(self):
        outs = {}
        sentinel = os.path.join(self.sentinel_dir,"sentinel_"+str(self))
        outs["sentinel"] = LocalTarget(sentinel)
        if self.dst_host:
            outs["dst"] = RemoteTarget(self.dst,self.dst_host)
        else:
            outs["dst"] = LocalTarget(self.dst)
        return outs

    def run(self):
        outs = self.output()
        # build command
        cmd = ["rsync"] + shlex.split(self.opts)
        srcparts = []
        if self.src_host:
            if self.src_user:
                srcparts.append(self.src_user)
                srcparts.append("@")
            srcparts.append(self.src_host)
            srcparts.append(":")
        srcparts.append(self.src)
        cmd.append("".join(srcparts))

        dstparts = []
        if self.dst_host:
            if self.dst_user:
                dstparts.append(self.dst_user)
                dstparts.append("@")
            dstparts.append(self.dst_host)
            dstparts.append(":")
        dstparts.append(self.dst)
        cmd.append("".join(dstparts))

        logger.debug("Calling %s"," ".join(cmd))
        p = subprocess32.Popen(cmd, stdout=subprocess32.PIPE,
                               stderr=subprocess32.STDOUT,
                               bufsize=1, #line buffered
                               universal_newlines=True)
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                logger.info("%s %s"%(self.task_id,line.rstrip()))

        if p.returncode != 0:
            raise IncompleteException("rsync existed with status %d"%p.returncode)

        # touch sentinel
        with outs["sentinel"].open('w'): pass

        # note that this only checks for the top-level dir
        if not self.complete():
            raise IncompleteException("rsync failed")

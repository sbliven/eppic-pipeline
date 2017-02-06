import luigi
from luigi import Task,Parameter,LocalTarget,ExternalTask
import urllib2
import subprocess
import logging
from luigi.contrib.ssh import RemoteTarget

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
    opts = Parameter(description="options passed to rsync",default="-az")
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
        if self.dst_host:
            yield RemoteTarget(self.dst,self.dst_host)
        else:
            yield LocalTarget(self.dst)

    def run(self):
        # build command
        cmd = ["rsync", self.opts]
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
        rtn = subprocess.call(cmd)

        if rtn:
            raise IncompleteException("rsync existed with status %d"%rtn)

        # note that this only checks for the top-level dir
        if not self.complete():
            raise IncompleteException("rsync failed")

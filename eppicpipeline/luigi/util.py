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
    user = Parameter(default="")

    def output(self):
        #TODO also accepts parameters: username, key_file, connect_timeout, port,
        # no_host_key_check, sshpass, and tty (See luigi.contrib.ssh.RemoteContext)
        return RemoteTarget(self.filename,self.host,username=self.user if self.user else None)

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

    Also note that src should end with at / if it is a directory.
    """
    opts = Parameter(description="options passed to rsync",default="-az")
    src = Parameter()
    dst = Parameter()
    src_host = Parameter(default="")
    src_user = Parameter(default="")
    dst_host = Parameter(default="")
    dst_user = Parameter(default="")
    def __init__(self,*args,**kwargs):
        super(RsyncTask,self).__init__(*args,**kwargs)
        self._has_run = False
    def requires(self):
        if self.src_host:
            yield RemoteExternalFile(filename=self.src,host=self.src_host,user=self.src_user)
        else:
            yield ExternalFile(filename=self.src)

    def output(self):
        if self.dst_host:
            yield RemoteTarget(self.dst,self.dst_host,user=self.dst_user)
        else:
            yield LocalTarget(self.dst)

    def complete(self):
        #TODO work out how to do this
        return True
        return self._has_run and super(RsyncTask,self).complete()

    def run(self):
        self._has_run = True

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
        #if not all(o.exists() for o in self.output()):
        if not self.complete():
            raise IncompleteException("rsync failed")

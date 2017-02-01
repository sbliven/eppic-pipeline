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
    path = Parameter()
    def output(self):
        return LocalTarget(self.path)

class RemoteExternalFile(ExternalTask):
    path = Parameter()
    host = Parameter()

    def output(self):
        return RemoteTarget(self.path,self.host)

class CachedRemoteFile(Task):
    """Download a remote file to a known local location"""
    path = Parameter(description="Local path")
    url = Parameter(description="URL to download the file",significant=False)

    def output(self):
        return LocalTarget(self.path)

    def run(self):
        logger.info("Downloading {url} to {path}".format(**self.__dict__))
        response = urllib2.urlopen(self.url)
        chunksize = 1024
        with self.output().open('wb') as tmp:
            for chunk in iter(lambda: response.read(chunksize), ''):
                tmp.write(chunk)

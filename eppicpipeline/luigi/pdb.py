"""Tasks for interacting with the pdb
"""
from luigi import Task,Parameter,LocalTarget
import urllib2

class PdbList(Task):
    """Download the list of current PDB IDs
    """
    url = Parameter(default="http://www.rcsb.org/pdb/rest/getCurrent", significant=False)
    output_list = Parameter(description="Filename for the PDB list")

    def output(self):
        return LocalTarget(self.output_list)

    def run(self):
        #XML available at http://www.rcsb.org/pdb/rest/getCurrent
        #<PDB structureId="100D" />

        response = urllib2.urlopen(self.url)
        with self.output().open('w') as out:
            for line in response:
                i = line.find("structureId=")
                if i >= 0:
                    pdb = line[i+13:i+17]
                    out.write(pdb+"\n")

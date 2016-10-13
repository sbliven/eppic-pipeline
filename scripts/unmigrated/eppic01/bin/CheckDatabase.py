'''
Created on Jan 22, 2015

@author: baskaran_k
'''


from commands import getstatusoutput
import MySQLdb
import sys
class CheckDatabase:
    
    
    def __init__(self,database,outfolder):
        self.outFolder=outfolder
        self.mysqluser='eppicweb'
        self.mysqlhost='localhost'
        self.mysqlpasswd='prdbpw+e01'
        self.database=database
        self.cnx=MySQLdb.connect(user=self.mysqluser,host=self.mysqlhost,passwd=self.mysqlpasswd,db=self.database,local_infile=True)
        self.cifrepo='/data/dbs/pdb/data/structures/all/mmCIF'
        self.getPDBlist()
        self.getDatabaselist()
        self.findMissing()
        self.printOutput()
        self.writeFiles()
    
    def getPDBlist(self):
        getlist=getstatusoutput("ls %s/ | sed 's/.cif.gz//g'"%(self.cifrepo))
        if getlist[0]:
            print "Can't get the list from cifrep"
            sys.exit(1)
        else:
            self.pdblist=getlist[1].split("\n")
    
    def getDatabaselist(self):
        c=self.cnx.cursor()
        mysqlcmd="select inputName from Job where submissionId<0 "
        c.execute(mysqlcmd)
        self.eppiclist=[i[0] for i in c.fetchall()]
        mysqlcmd="select inputName from Job where submissionId<0 and status != 'Finished'"
        c.execute(mysqlcmd)
        self.eppicErrorlist=[i[0] for i in c.fetchall()]
        
    def findMissing(self):
        self.missing=list(set(self.pdblist)-set(self.eppiclist))
        self.obsolete=list(set(self.eppiclist)-set(self.pdblist))
    
    def printOutput(self):
        print "\tTotal No. of entries in the PDB repo \t\t%d"%(len(self.pdblist))
        print "\tTotal No. of entries in the EPPIC db \t\t%d"%(len(self.eppiclist))
        print "\tNo. of entries with error in EPPIC db \t\t%s"%(len(self.eppicErrorlist))
        print "\tNo. of entries missing in EPPIC db \t\t%s"%(len(self.missing))
        print "\tNo. of obsoleted entries exists in EPPIC db \t%s"%(len(self.obsolete))
    
    def writeFiles(self):
        open("%s/pdbrepo.list"%(self.outFolder),'w').write("%s\n"%("\n".join(self.pdblist)))
        open("%s/eppicdb.list"%(self.outFolder),'w').write("%s\n"%("\n".join(self.eppiclist)))
        open("%s/eppicerror.list"%(self.outFolder),'w').write("%s\n"%("\n".join(self.eppicErrorlist)))
        open("%s/eppicmissing.list"%(self.outFolder),'w').write("%s\n"%("\n".join(self.missing)))
        open("%s/obsolete.list"%(self.outFolder),'w').write("%s\n"%("\n".join(self.obsolete)))
        
        
        
        
if __name__=="__main__":
    db=sys.argv[1]
    path=sys.argv[2]
    p=CheckDatabase(db,path)
    
    

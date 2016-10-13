import sys,os
from string import atoi,atof
import commands
def get_stat(dbname):
	cmd="mysql %s -N -B -e 'select count(*) from Job where length(jobId)=4'"%(dbname)
	PdbCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Job where length(jobId)=4 and status=\"Finished\"'"%(dbname) 
	EppicCount=atof(commands.getoutput(cmd))
	EppicCountp=(EppicCount/PdbCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from InterfaceScore as s inner join Interface as i on i.uid=s.interfaceItem_uid inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and s.method=\"eppic\"'"%(dbname)
	InterfaceCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from InterfaceScore as s inner join Interface as i on i.uid=s.interfaceItem_uid inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and s.method=\"eppic\" and s.callName=\"bio\"'"%(dbname)
	BioCount=atof(commands.getoutput(cmd))
	BioCountp=(BioCount/InterfaceCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from InterfaceScore as s inner join Interface as i on i.uid=s.interfaceItem_uid inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and s.method=\"eppic\" and s.callName=\"xtal\"'"%(dbname)
	XtalCount=atof(commands.getoutput(cmd))
	XtalCountp=(XtalCount/InterfaceCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4'"%(dbname)
	ChainCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and c.hasUniProtRef'"%(dbname)
	ChainHasUniprot=atof(commands.getoutput(cmd))
	ChainHasUniprotp=(ChainHasUniprot/ChainCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and c.hasUniProtRef and c.seqIdCutoff>0.59 and c.numHomologs>=10'"%(dbname)
	ChainHas10H60P=atof(commands.getoutput(cmd))
	ChainHas10H60Pp=(ChainHas10H60P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select count(*) from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and c.hasUniProtRef and c.seqIdCutoff>0.59 and c.numHomologs>=30'"%(dbname)
        ChainHas30H60P=atof(commands.getoutput(cmd))
        ChainHas30H60Pp=(ChainHas30H60P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select count(*) from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and c.hasUniProtRef and c.seqIdCutoff>0.59 and c.numHomologs>=50'"%(dbname)
        ChainHas50H60P=atof(commands.getoutput(cmd))
        ChainHas50H60Pp=(ChainHas50H60P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select count(*) from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and c.hasUniProtRef and c.seqIdCutoff>0.49 and c.numHomologs>=10'"%(dbname)
	ChainHas10H50P=atof(commands.getoutput(cmd))
	ChainHas10H50Pp=(ChainHas10H50P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select expMethod,count(*) from PdbInfo as p inner join Job as j on j.uid=p.job_uid where length(jobId)=4 group by p.expMethod order by count(*) desc'"%(dbname)
	ExpStat=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbCode,p.expMethod,i.interfaceId,i.area from Interface as i inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 order by i.area desc limit 10'"%(dbname)
	Top10Area=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbCode,p.expMethod,i.interfaceId,s.score from InterfaceScore as s inner join Interface as i on i.uid=s.interfaceItem_uid inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and s.method=\"eppic-gm\" order by s.score desc limit 10'"%(dbname)
	Top10Core=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbCode,p.expMethod,count(*) from InterfaceScore as s inner join Interface as i on i.uid=s.interfaceItem_uid inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and s.method=\"eppic\" group by s.pdbCode order by count(*) desc limit 10'"%(dbname)
	Top10inter=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbCode,p.expMethod,i.interfaceId,s.score from InterfaceScore as s inner join Interface as i on i.uid=s.interfaceItem_uid inner join InterfaceCluster as ic on ic.uid=i.interfaceCluster_uid inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 and s.method=\"eppic-cs\" and s.score is not NULL and s.score > -499 and s.callName!=\"nopred\" order by s.score limit 10'"%(dbname)
	Top10eppic=commands.getoutput(cmd).split("\n")
#	cmd="mysql %s -N -B -e 'select uniprot_2014_05.get_taxonomy(refUniProtId),count(*) count from ChainCluster c inner join PdbInfo as p on p.uid=c.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4' and c.hasUniProtRef group by  uniprot_2014_05.get_taxonomy(uniprotId) order by count(*) desc'"%(dbname)
#	Taxonomy=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbCode,p.expMethod,ic.clusterId,ic.numMembers from InterfaceCluster as ic inner join PdbInfo as p on p.uid=ic.pdbInfo_uid inner join Job as j on j.uid=p.job_uid where length(jobId)=4 order by ic.numMembers desc limit 10'"%(dbname)
	Top10Clusters=commands.getoutput(cmd).split("\n")

	
	print "\t\t\tStatistics from EPPIC precomputed database (EPPIC db) "
	print
	print "\t\t\tNumber of entries  "
	print "\t \tTotal number of entries in the PDB    \t\t\t%.0f   "%(PdbCount)
	print "\t \tTotal number of PDB entries in EPPIC db  \t\t%.0f  (%0.2f %%)   "%(EppicCount,EppicCountp)
	print
	print "\t\t\tInterface statistics  "
	print "\t \tTotal number of interfaces in EPPIC db  \t\t%.0f   "%(InterfaceCount)
	print "\t \tTotal number of interfaces classified as bio  \t\t%.0f  (%0.2f %%)   "%(BioCount,BioCountp)
	print "\t \tTotal number of interfaces classified as xtal  \t\t%.0f  (%0.2f %%)   "%(XtalCount,XtalCountp)
	print
	print "\t\t\tChain and homolog statistics  "
	print "\t \tTotal number of chains in EPPIC db \t\t\t\t\t\t%.0f   "%(ChainCount)
	print "\t \tTotal number of chains with UniProt match \t\t\t\t\t%.0f  (%0.2f %%)   "%(ChainHasUniprot,ChainHasUniprotp)
	print "\t \tTotal number of chains having at least 10 homologs with 50%% sequence identity\t%.0f  (%0.2f %%)   "%(ChainHas10H50P,ChainHas10H50Pp)
	print "\t \tTotal number of chains having at least 10 homologs with 60%% sequence identity\t%.0f  (%0.2f %%)   "%(ChainHas10H60P,ChainHas10H60Pp)
	print "\t \tTotal number of chains having at least 30 homologs with 60%% sequence identity\t%.0f  (%0.2f %%)   "%(ChainHas30H60P,ChainHas30H60Pp)
	print "\t \tTotal number of chains having at least 50 homologs with 60%% sequence identity\t%.0f  (%0.2f %%)   "%(ChainHas50H60P,ChainHas50H60Pp)
	print 
#	print "\t\t\tTaxonomic distribution in EPPIC db  ")
#          
        #print "\t<tr><td width=\"200\"><b>Taxonomy\t No. of chains     ")
#        for ent in Taxonomy:
#                val=ent.split("\t")
#                print "\t<tr><td width=\"200\">%s  %.0f  (%.2f %%)   "%(val[0],atof(val[1]),100*(atof(val[1])/ChainHasUniprot)))
#           
	
	print "\t\t\tInterface area statistics (Top 10)  "
	print "\t\tPDBId\tExp.method\tInterfaceId\tInterface area     "
	for ent in Top10Area:
		val=ent.split("\t")
		print "\t\t%s\t%s\t%.0f\t%0.2f   \t   "%(val[0],val[1],atof(val[2]),atof(val[3]))
	print
	print "\t\t\tCore residues statistics (Top 10)  "
	print "\t\tPDBId\tExp.method\tInterfaceId\tTotal no. of core residues     "
	for ent in Top10Core:
		val=ent.split("\t")
		print "\t\t%s\t%s\t%.0f\t%.0f   "%(val[0],val[1],atof(val[2]),atof(val[3]))
	print
	print "\t\t\tMaximum number of interfaces in a single PDB entry (Top 10)  "
	print "\t\tPDBId\tExp.method\tTotal no. of Interfaces     "
	for ent in Top10inter:
		val=ent.split("\t")
		print "\t\t%s\t%s\t%.0f   "%(val[0],val[1],atof(val[2]))
	print
	print "\t\t\tLargest interface clusters in a single PDB entry (Top 10)  " 
        print "\t\tPDBId\tExp.method\tClusterId\tCluster size     "
        for ent in Top10Clusters:
                val=ent.split("\t")
                print "\t\t%s\t%s\t%.0f\t%.0f   "%(val[0],val[1],atof(val[2]),atof(val[3]))
	print
	print "\t\t\tHighly conserved interfaces based on Eppic evolutionary score (Top 10)  "
	print "\t\tPDBId\tExp.method\tInterfaceId\tCore-surface score     "
	for ent in Top10eppic:
		val=ent.split("\t")
		print "\t\t%s\t%s\t%.0f\t%0.2f   "%(val[0],val[1],atof(val[2]),atof(val[3]))
	print
	print "\t\t\tExperimental technique statistics  "
	for ent in ExpStat:
		val=ent.split("\t")
		print "\t\t%27s\t\t\t%.0f\t(%0.2f %%)   "%(val[0],atof(val[1]),(atof(val[1])/EppicCount)*100)
	print
	
	
	
if __name__=="__main__":
	dbname=sys.argv[1]
	get_stat(dbname)	








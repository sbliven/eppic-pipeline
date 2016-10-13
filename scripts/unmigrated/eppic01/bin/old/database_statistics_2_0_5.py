import sys,os
from string import atoi,atof
import commands
def get_stat(dbname):
	cmd="mysql %s -N -B -e 'select count(*) from Job where length(jobId)=4'"%(dbname)
	PdbCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Job where length(jobId)=4 and status=\"Finished\"'"%(dbname) 
	EppiCcount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4'"%(dbname)
	InterfaceCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and i.finalCallName=\"bio\"'"%(dbname)
	BioCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and i.finalCallName=\"xtal\"'"%(dbname)
	XtalCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4'"%(dbname)
	ChainCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch'"%(dbname)
	ChainHasUniprot=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch and h.idCutoffUsed>0.59 and h.numHomologs>=10'"%(dbname)
	ChainHas10H60P=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch and h.idCutoffUsed>0.49 and h.numHomologs>=10'"%(dbname)
	ChainHas10H50P=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select expMethod,count(*) from PdbScore as p inner join Job as j on j.uid=p.jobItem_uid where length(j.jobId)=4 group by p.expMethod order by count(*) desc'"%(dbname)
	ExpStat=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select spaceGroup,count(*) from PdbScore as p inner join Job as j on j.uid=p.jobItem_uid where length(j.jobId)=4 and p.spaceGroup is not NULL group by p.spaceGroup order by count(*) desc'"%(dbname)
	SpacegroupStat=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,i.id,i.area from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 order by area desc limit 10'"%(dbname)
	Top10Area=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,i.id,i.size1+i.size2 from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 order by (i.size1+i.size2) desc limit 10'"%(dbname)
	Top10Core=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 group by i.pdbScoreItem_uid order by count(*) desc limit 10'"%(dbname)
	Top10inter=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,i.id,ic.unweightedFinalScores from InterfaceScore as ic inner join Interface as i on ic.interfaceItem_uid=i.uid inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and ic.method=\"Z-scores\" and ic.unweightedFinalScores is not NULL and ic.unweightedFinalScores > -499 and ic.callName!=\"nopred\" order by ic.unweightedFinalScores limit 10'"%(dbname)
	Top10eppic=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,i.id,ic.unweightedFinalScores from InterfaceScore as ic inner join Interface as i on ic.interfaceItem_uid=i.uid inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and ic.method=\"Z-scores\" and ic.unweightedFinalScores is not NULL and ic.unweightedFinalScores < 490 and ic.callName!=\"nopred\" order by ic.unweightedFinalScores desc limit 10'"%(dbname)
	Top10eppic2=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,i.id,ic.unweightedFinalScores from InterfaceScore as ic inner join Interface as i on ic.interfaceItem_uid=i.uid inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and ic.method=\"Entropy\" and ic.unweightedFinalScores is not NULL and ic.unweightedFinalScores > -499 and ic.callName!=\"nopred\" order by ic.unweightedFinalScores limit 10'"%(dbname)
	Top10eppic3=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,i.id,ic.unweightedFinalScores from InterfaceScore as ic inner join Interface as i on ic.interfaceItem_uid=i.uid inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and ic.method=\"Entropy\" and ic.unweightedFinalScores is not NULL and ic.unweightedFinalScores < 490 and ic.callName!=\"nopred\" order by ic.unweightedFinalScores desc limit 10'"%(dbname)
	Top10eppic4=commands.getoutput(cmd).split("\n")

	print 
	print "\t================================ Statistics on %s database==============================="%(dbname)
	print "\tTotal number of PDBs in the database\t\t\t\t\t=\t",PdbCount
	print "\tTotal number of PDBs with EPPIC results\t\t\t\t\t=\t",EppiCcount,"(",(EppiCcount/PdbCount)*100,"%)"
	print
	print "\t========================== Interface Statistics=================================================="
	print "\tTotal number of Interfaces\t\t\t\t\t\t=\t",InterfaceCount
	print "\tTotal number of Bio Interfaces\t\t\t\t\t\t=\t",BioCount,"(",(BioCount/InterfaceCount)*100,"%)"
	print "\tTotal number of Xtal Interfaces\t\t\t\t\t\t=\t",XtalCount,"(",(XtalCount/InterfaceCount)*100,"%)"
	print
	print "\t========================== Chain Statistics=================================================="
	print "\tTotal number of Chains\t\t\t\t\t\t\t=\t",ChainCount
	print "\tTotal number of Chains having Uniprot mapping\t\t\t\t=\t",ChainHasUniprot,"(",(ChainHasUniprot/ChainCount)*100,"%)"
	print "\tTotal number of Chains having atleast 10 homologs and 60% seq identity\t=\t",ChainHas10H60P,"(",(ChainHas10H60P/ChainHasUniprot)*100,"%)"
	print "\tTotal number of Chains having atleast 10 homologs and 50% seq identity\t=\t",ChainHas10H50P,"(",(ChainHas10H50P/ChainHasUniprot)*100,"%)"
	print
	print "\t========================== Experiment Statistics=================================================="
	for i in ExpStat:
		w=i.split("\t")
		print "\t%30s\t\t\t=\t%f\t(%f)"%(w[0],atof(w[1]),100*(atof(w[1])/PdbCount))
	print
	print "\t========================== Space group Statistics=================================================="
	sume=sum([atof(i.split("\t")[1]) for i in SpacegroupStat])
	for i in SpacegroupStat:
		w=i.split("\t")
		print "\t%15s\t\t\t=\t%f\t(%f)"%(w[0],atof(w[1]),100*(atof(w[1])/sume))
	print
	print "\t========================== Top 10 =================================================="
	print "\t%6s\t\t%s\t\t%s"%("PDBId","InterfaceId","Area")
	for i in Top10Area:
		w=i.split("\t")
		print "\t%6s\t\t%s\t\t%s"%(w[0],w[1],w[2])
	print
	print "\t========================== Top 10=================================================="
	print "\t%6s\t\t%s\t%s"%("PDBId","InterfaceId","Core residues")
	for i in Top10Core:
		w=i.split("\t")
		print "\t%6s\t\t%s\t\t%s"%(w[0],w[1],w[2])
	print
	print "\t========================== Top 10 =================================================="
	print "\t%6s\t\t%s"%("PDBId","No. Interfaces > 35A")
	for i in Top10inter:
		w=i.split("\t")
		print "\t%6s\t\t%s"%(w[0],w[1])
	print
	print "\t========================== Top 10(best)=================================================="
	print "\t%6s\t\t%s\t%s"%("PDBId","InterfaceId","CS score")
	for i in Top10eppic:
		w=i.split("\t")
		print "\t%6s\t\t%s\t\t%s"%(w[0],w[1],w[2])
	print
	print "\t========================== Top 10(worst)=================================================="
	print "\t%6s\t\t%s\t%s"%("PDBId","InterfaceId","CS score")
	for i in Top10eppic2:
		w=i.split("\t")
		print "\t%6s\t\t%s\t\t%s"%(w[0],w[1],w[2])
	print
	print "\t========================== Top 10(best)=================================================="
	print "\t%6s\t\t%s\t%s"%("PDBId","InterfaceId","CR score")
	for i in Top10eppic3:
		w=i.split("\t")
		print "\t%6s\t\t%s\t\t%s"%(w[0],w[1],w[2])
	print
	print "\t========================== Top 10(worst)=================================================="
	print "\t%6s\t\t%s\t%s"%("PDBId","InterfaceId","CR score")
	for i in Top10eppic4:
		w=i.split("\t")
		print "\t%6s\t\t%s\t\t%s"%(w[0],w[1],w[2])
	print
if __name__=="__main__":
	dbname=sys.argv[1]
	get_stat(dbname)	








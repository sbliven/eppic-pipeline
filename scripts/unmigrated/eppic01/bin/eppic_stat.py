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

	#fo=open("eppic_statistics.html",'w')
	print ("<!DOCTYPE html>\n<html>\n")
	print ("<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.eppic-web.org/ewui/eppic-static.css\">\n<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,700,400italic,700italic' rel='stylesheet' type='text/css'>\n</head>\n")
	print ("<body>\n") 
	print ("\t<center><h1>Statistics from EPPIC precomputed database (EPPIC db)</h1></center>\n")

	print ("\t<h2>Number of entries</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"600\">Total number of entries in the <a href=\"http://www.pdb.org/pdb/home/home.do\">PDB</a></td><td width=\"60\">%.0f</td></tr>\n"%(PdbCount))
	print ("\t<tr><td width=\"600\">Total number of PDB entries in EPPIC db</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(EppicCount,EppicCountp))
	print ("\t</table></center>\n")

	print ("\t<h2>Interface statistics</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"600\">Total number of interfaces in EPPIC db</td><td width=\"60\">%.0f</td></tr>\n"%(InterfaceCount))
	print ("\t<tr><td width=\"600\">Total number of interfaces classified as bio</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(BioCount,BioCountp))
	print ("\t<tr><td width=\"600\">Total number of interfaces classified as xtal</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(XtalCount,XtalCountp))
	print ("\t</table></center>\n")
	
	print ("\t<h2>Chain and homolog statistics</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"600\">Total number of chains in EPPIC db</td><td width=\"60\">%.0f</td></tr>\n"%(ChainCount))
	print ("\t<tr><td width=\"600\">Total number of chains with UniProt match</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHasUniprot,ChainHasUniprotp))
	print ("\t<tr><td width=\"600\">Total number of chains having at least 10 homologs with 50%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas10H50P,ChainHas10H50Pp))
	print ("\t<tr><td width=\"600\">Total number of chains having at least 10 homologs with 60%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas10H60P,ChainHas10H60Pp))
	print ("\t<tr><td width=\"600\">Total number of chains having at least 30 homologs with 60%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas30H60P,ChainHas30H60Pp))
	print ("\t<tr><td width=\"600\">Total number of chains having at least 50 homologs with 60%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas50H60P,ChainHas50H60Pp))
	print ("\t</table></center>\n")
#	print ("\t<h2>Taxonomic distribution in EPPIC db</h2>\n")
#        print ("\t<center><table>\n")
        #print ("\t<tr><td width=\"200\"><b>Taxonomy</b></td><td width=\"100\"><b>No. of chains</b></td></tr>\n")
#        for ent in Taxonomy:
#                val=ent.split("\t")
#                print ("\t<tr><td width=\"200\">%s</td><td width=\"60\">%.0f</td><td width=\"80\">(%.2f %%)</td></tr>\n"%(val[0],atof(val[1]),100*(atof(val[1])/ChainHasUniprot)))
#        print ("\t</table></center>\n")
	
	print ("\t<h2>Interface area statistics (Top 10)</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>InterfaceId</b></td><td width=\"300\"><b>Interface area</b></td></tr>\n")
	for ent in Top10Area:
		val=ent.split("\t")
		print ("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"100\">%.0f</td><td width=\"300\">%0.2f &Aring<sup>2</sup></td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	print ("\t</table></center>\n")

	print ("\t<h2>Core residues statistics (Top 10)</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>InterfaceId</b></td><td width=\"300\"><b>Total no. of core residues</b></td></tr>\n")
	for ent in Top10Core:
		val=ent.split("\t")
		print ("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"100\">%.0f</td><td width=\"300\">%.0f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	print ("\t</table></center>\n")

	print ("\t<h2>Maximum number of interfaces in a single PDB entry (Top 10)</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"300\"><b>Total no. of Interfaces</b></td></tr>\n")
	for ent in Top10inter:
		val=ent.split("\t")
		print ("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"300\">%.0f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2])))
	print ("\t</table></center>\n")
	

	print ("\t<h2>Largest interface clusters in a single PDB entry (Top 10)</h2>\n")
        print ("\t<center><table>\n")
        print ("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>ClusterId</b></td><td width=\"100\"><b>Cluster size</b></td></tr>\n")
        for ent in Top10Clusters:
                val=ent.split("\t")
                print ("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"100\">%s</td><td width=\"100\">%.0f</td><td width=\"100\">%.0f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
        print ("\t</table></center>\n")

	print ("\t<h2>Highly conserved interfaces based on Eppic evolutionary score (Top 10)</h2>\n")
	print ("\t<center><table>\n")
	print ("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>InterfaceId</b></td><td width=\"300\"><b>Core-surface score</b></td></tr>\n")
	for ent in Top10eppic:
		val=ent.split("\t")
		print ("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"100\">%.0f</td><td width=\"300\">%0.2f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	print ("\t</table></center>\n")

	print ("\t<h2>Experimental technique statistics</h2>\n")
	print ("\t<center><table>\n")
	for ent in ExpStat:
		val=ent.split("\t")
		print ("\t<tr><td width=\"600\">%s</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(val[0],atof(val[1]),(atof(val[1])/EppicCount)*100))
	print ("\t</table></center>\n")
	print ("\n\n\n\t <center><b>For the RCSB PDB statistics page, click <a href=\"http://www.pdb.org/pdb/static.do?p=general_information/pdb_statistics/index.html\">here</a></b></center>\n") 	
	print ("</body>\n</html>")
	
	
if __name__=="__main__":
	dbname=sys.argv[1]
	get_stat(dbname)	








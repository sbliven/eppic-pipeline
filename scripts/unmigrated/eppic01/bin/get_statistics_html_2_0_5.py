import sys,os
from string import atoi,atof
import commands
def get_stat(dbname):
	cmd="mysql %s -N -B -e 'select count(*) from Job where length(jobId)=4'"%(dbname)
	PdbCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Job where length(jobId)=4 and status=\"Finished\"'"%(dbname) 
	EppicCount=atof(commands.getoutput(cmd))
	EppicCountp=(EppicCount/PdbCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4'"%(dbname)
	InterfaceCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and i.finalCallName=\"bio\"'"%(dbname)
	BioCount=atof(commands.getoutput(cmd))
	BioCountp=(BioCount/InterfaceCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and i.finalCallName=\"xtal\"'"%(dbname)
	XtalCount=atof(commands.getoutput(cmd))
	XtalCountp=(XtalCount/InterfaceCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4'"%(dbname)
	ChainCount=atof(commands.getoutput(cmd))
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch'"%(dbname)
	ChainHasUniprot=atof(commands.getoutput(cmd))
	ChainHasUniprotp=(ChainHasUniprot/ChainCount)*100
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch and h.idCutoffUsed>0.59 and h.numHomologs>=10'"%(dbname)
	ChainHas10H60P=atof(commands.getoutput(cmd))
	ChainHas10H60Pp=(ChainHas10H60P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch and h.idCutoffUsed>0.59 and h.numHomologs>=30'"%(dbname)
        ChainHas30H60P=atof(commands.getoutput(cmd))
        ChainHas30H60Pp=(ChainHas30H60P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch and h.idCutoffUsed>0.59 and h.numHomologs>=50'"%(dbname)
        ChainHas50H60P=atof(commands.getoutput(cmd))
        ChainHas50H60Pp=(ChainHas50H60P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select count(*) from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch and h.idCutoffUsed>0.49 and h.numHomologs>=10'"%(dbname)
	ChainHas10H50P=atof(commands.getoutput(cmd))
	ChainHas10H50Pp=(ChainHas10H50P/ChainHasUniprot)*100
	cmd="mysql %s -N -B -e 'select expMethod,count(*) from PdbScore as p inner join Job as j on j.uid=p.jobItem_uid where length(j.jobId)=4 group by p.expMethod order by count(*) desc'"%(dbname)
	ExpStat=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,p.expMethod,i.id,i.area from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 order by area desc limit 10'"%(dbname)
	Top10Area=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,p.expMethod,i.id,i.size1+i.size2 from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 order by (i.size1+i.size2) desc limit 10'"%(dbname)
	Top10Core=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,p.expMethod,count(*) from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 group by i.pdbScoreItem_uid order by count(*) desc limit 10'"%(dbname)
	Top10inter=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,p.expMethod,i.id,ic.unweightedFinalScores from InterfaceScore as ic inner join Interface as i on ic.interfaceItem_uid=i.uid inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and ic.method=\"Z-scores\" and ic.unweightedFinalScores is not NULL and ic.unweightedFinalScores > -499 and ic.callName!=\"nopred\" order by ic.unweightedFinalScores limit 10'"%(dbname)
	Top10eppic=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select uniprot_2014_05.get_taxonomy(uniprotId),count(*) count from HomologsInfoItem as h inner join PdbScore as p on p.uid=h.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 and h.hasQueryMatch group by  uniprot_2014_05.get_taxonomy(uniprotId) order by count(*) desc'"%(dbname)
	Taxonomy=commands.getoutput(cmd).split("\n")
	cmd="mysql %s -N -B -e 'select p.pdbName,p.expMethod,i.clusterId,count(*) count from Interface as i inner join PdbScore as p on p.uid=i.pdbScoreItem_uid inner join Job as j on j.uid=p.jobItem_uid where length(jobId)=4 group by i.pdbScoreItem_uid,i.clusterId order by count(*) desc limit 10'"%(dbname)
	Top10Clusters=commands.getoutput(cmd).split("\n")

	fo=open("eppic_statistics.html",'w')
	fo.write("<!DOCTYPE html>\n<html>\n")
	fo.write("<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"http://www.eppic-web.org/ewui/eppic-static.css\">\n<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,700,400italic,700italic' rel='stylesheet' type='text/css'>\n</head>\n")
	fo.write("<body>\n") 
	fo.write("\t<center><h1>Statistics from EPPIC precomputed database (EPPIC db)</h1></center>\n")

	fo.write("\t<h2>Number of entries</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"600\">Total number of entries in the <a href=\"http://www.pdb.org/pdb/home/home.do\">PDB</a></td><td width=\"60\">%.0f</td></tr>\n"%(PdbCount))
	fo.write("\t<tr><td width=\"600\">Total number of PDB entries in EPPIC db</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(EppicCount,EppicCountp))
	fo.write("\t</table></center>\n")

	fo.write("\t<h2>Interface statistics</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"600\">Total number of interfaces in EPPIC db</td><td width=\"60\">%.0f</td></tr>\n"%(InterfaceCount))
	fo.write("\t<tr><td width=\"600\">Total number of interfaces classified as bio</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(BioCount,BioCountp))
	fo.write("\t<tr><td width=\"600\">Total number of interfaces classified as xtal</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(XtalCount,XtalCountp))
	fo.write("\t</table></center>\n")
	
	fo.write("\t<h2>Chain and homolog statistics</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"600\">Total number of chains in EPPIC db</td><td width=\"60\">%.0f</td></tr>\n"%(ChainCount))
	fo.write("\t<tr><td width=\"600\">Total number of chains with UniProt match</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHasUniprot,ChainHasUniprotp))
	fo.write("\t<tr><td width=\"600\">Total number of chains having at least 10 homologs with 50%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas10H50P,ChainHas10H50Pp))
	fo.write("\t<tr><td width=\"600\">Total number of chains having at least 10 homologs with 60%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas10H60P,ChainHas10H60Pp))
	fo.write("\t<tr><td width=\"600\">Total number of chains having at least 30 homologs with 60%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas30H60P,ChainHas30H60Pp))
	fo.write("\t<tr><td width=\"600\">Total number of chains having at least 50 homologs with 60%% sequence identity</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(ChainHas50H60P,ChainHas50H60Pp))
	fo.write("\t</table></center>\n")
	fo.write("\t<h2>Taxonomic distribution in EPPIC db</h2>\n")
        fo.write("\t<center><table>\n")
        #fo.write("\t<tr><td width=\"200\"><b>Taxonomy</b></td><td width=\"100\"><b>No. of chains</b></td></tr>\n")
        for ent in Taxonomy:
                val=ent.split("\t")
                fo.write("\t<tr><td width=\"200\">%s</td><td width=\"60\">%.0f</td><td width=\"80\">(%.2f %%)</td></tr>\n"%(val[0],atof(val[1]),100*(atof(val[1])/ChainHasUniprot)))
        fo.write("\t</table></center>\n")
	
	fo.write("\t<h2>Interface area statistics (Top 10)</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>InterfaceId</b></td><td width=\"300\"><b>Interface area</b></td></tr>\n")
	for ent in Top10Area:
		val=ent.split("\t")
		fo.write("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"100\">%.0f</td><td width=\"300\">%0.2f &Aring<sup>2</sup></td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	fo.write("\t</table></center>\n")

	fo.write("\t<h2>Core residues statistics (Top 10)</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>InterfaceId</b></td><td width=\"300\"><b>Total no. of core residues</b></td></tr>\n")
	for ent in Top10Core:
		val=ent.split("\t")
		fo.write("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"100\">%.0f</td><td width=\"300\">%.0f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	fo.write("\t</table></center>\n")

	fo.write("\t<h2>Maximum number of interfaces in a single PDB entry (Top 10)</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"300\"><b>Total no. of Interfaces</b></td></tr>\n")
	for ent in Top10inter:
		val=ent.split("\t")
		fo.write("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"300\">%.0f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2])))
	fo.write("\t</table></center>\n")
	

	fo.write("\t<h2>Largest interface clusters in a single PDB entry (Top 10)</h2>\n")
        fo.write("\t<center><table>\n")
        fo.write("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>ClusterId</b></td><td width=\"100\"><b>Cluster size</b></td></tr>\n")
        for ent in Top10Clusters:
                val=ent.split("\t")
                fo.write("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"100\">%s</td><td width=\"100\">%.0f</td><td width=\"100\">%.0f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
        fo.write("\t</table></center>\n")

	fo.write("\t<h2>Highly conserved interfaces based on Eppic evolutionary score (Top 10)</h2>\n")
	fo.write("\t<center><table>\n")
	fo.write("\t<tr><td width=\"100\"><b>PDBId</b></td><td width=\"200\"><b>Exp.method</b></td><td width=\"100\"><b>InterfaceId</b></td><td width=\"300\"><b>Core-surface score</b></td></tr>\n")
	for ent in Top10eppic:
		val=ent.split("\t")
		fo.write("\t<tr><td width=\"100\"><a href=\"http://eppic-web.org/ewui/#id/%s\">%s</a></td><td width=\"200\">%s</td><td width=\"100\">%.0f</td><td width=\"300\">%0.2f</td></tr>\n"%(val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	fo.write("\t</table></center>\n")

	fo.write("\t<h2>Experimental technique statistics</h2>\n")
	fo.write("\t<center><table>\n")
	for ent in ExpStat:
		val=ent.split("\t")
		fo.write("\t<tr><td width=\"600\">%s</td><td width=\"60\">%.0f</td><td width=\"80\">(%0.2f %%)</td></tr>\n"%(val[0],atof(val[1]),(atof(val[1])/EppicCount)*100))
	fo.write("\t</table></center>\n")
	fo.write("\n\n\n\t <center><b>For the RCSB PDB statistics page, click <a href=\"http://www.pdb.org/pdb/static.do?p=general_information/pdb_statistics/index.html\">here</a></b></center>\n") 	
	fo.write("</body>\n</html>")
	
	
if __name__=="__main__":
	dbname=sys.argv[1]
	get_stat(dbname)	








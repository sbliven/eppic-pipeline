import sys,os
from string import atoi,atof
from datetime import date
import commands
def get_stat(dbname,total,new,removed,uniprot,rsyncfile):
	updated=total-new
	rsyncdate=rsyncfile.split("_")[1].split(".log")[0].split("-")
	rdate="%s-%s-%s"%("%02d"%(atoi(rsyncdate[2])-1),rsyncdate[1],rsyncdate[0])
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
	today=date.today().strftime('%d-%m-%Y')
	prev_dat=dict((i.split("\t")[0],i.split("\t")[1]) for i in open("/home/eppicweb/topup/statistics_prev.txt",'r').read().split("\n")[:-1])
	
	fo=open("/home/eppicweb/topup/statistics.html",'w')
	fo.write("<!DOCTYPE html>\n<html>\n")
	fo.write("<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"eppic-static.css\">\n<link href='http://fonts.googleapis.com/css?family=Open+Sans:400,700,400italic,700italic' rel='stylesheet' type='text/css'>\n</head>\n")
	fo.write("<body>\n") 
	fo.write("\t<script type=\"text/javascript\">\n\t\tfunction reloadPage(url) {\n\t\t\twindow.top.location=url;\n\t\t}\n\t</script>\n")
	fo.write("\t<div class=\"eppic-iframe-content\">\n")
	fo.write("\t<img class=\"eppic-iframe-top-img\" src=\"resources/images/eppic-logo.png\">\n")
	fo.write("\t<div class=\"eppic-statistics\">\n")
	fo.write("\t<h1>EPPIC database statistics as of %s</h1>\n"%(today))
	fo.write("\t<h3>Based on UniProt_%s and PDB release of %s</h3>\n"%(uniprot,rdate))
	fo.write("\t<h4>Values in []: absolute and percentual difference between before and after top-up</h4>\n")

	fo.write("\t<h2>Number of entries</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><td class=\"text\">Total number of entries in the <a href=\"http://www.pdb.org/pdb/home/home.do\" target=\"_blank\">PDB</a></td><td class=\"numeric\">%.0f</td><td></td></tr>\n"%(PdbCount))
	fo.write("\t<tr><td class=\"text\">Total number of PDB entries in EPPIC db</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td></tr>\n"%(EppicCount,EppicCountp))
	fo.write("\t</table>\n")

	fo.write("\t<h2>Top-up on %s</h2>\n"%(today))
	fo.write("\t<table>\n")
	fo.write("\t<tr><td class=\"text\">New PDB entries </td><td class=\"numeric\">%.0f</td></tr>\n"%(new))
	fo.write("\t<tr><td class=\"text\">Updated PDB entries </td><td class=\"numeric\">%.0f</td></tr>\n"%(updated))
	fo.write("\t<tr><td class=\"text\">Deleted PDB entries (obsolete entries) </td><td class=\"numeric\">%.0f</td></tr>\n"%(removed))
	fo.write("\t</table>\n")
	
	InterfaceCountdiff=InterfaceCount-atoi(prev_dat['InterfaceCount'])
	if InterfaceCountdiff<0:
		InterfaceCountdiffc="neg_numeric"
	elif InterfaceCountdiff>0:
		InterfaceCountdiffc="pos_numeric"
	else:
		InterfaceCountdiffc="zero_numeric"
	BioCountdiff=BioCount-atoi(prev_dat['BioCount'])
	if BioCountdiff<0:
		BioCountdiffc="neg_numeric"
	elif BioCountdiff>0:
		BioCountdiffc="pos_numeric"
	else:
		BioCountdiffc="zero_numeric"
	BioCountpdiff=BioCountp-atof(prev_dat['BioCountp'])
	XtalCountdiff=XtalCount-atoi(prev_dat['XtalCount'])
	if XtalCountdiff<0:
		XtalCountdiffc="neg_numeric"
	elif XtalCountdiff>0:
		XtalCountdiffc="pos_numeric"
	else:
		XtalCountdiffc="zero_numeric"
	XtalCountpdiff=XtalCountp-atof(prev_dat['XtalCountp'])
	fo.write("\t<h2>Interface statistics</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><td class=\"text\">Total number of interfaces in EPPIC db</td><td class=\"numeric\">%.0f</td><td></td><td class=\"%s\">[%d]</td></tr>\n"%(InterfaceCount,InterfaceCountdiffc,InterfaceCountdiff))
	fo.write("\t<tr><td class=\"text\">Total number of interfaces classified as bio</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(BioCount,BioCountp,BioCountdiffc,BioCountdiff,round(BioCountpdiff,4)))
	fo.write("\t<tr><td class=\"text\">Total number of interfaces classified as xtal</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(XtalCount,XtalCountp,XtalCountdiffc,XtalCountdiff,round(XtalCountpdiff,4)))
	fo.write("\t</table>\n")
	
	ChainCountdiff=ChainCount-atoi(prev_dat['ChainCount'])
	if ChainCountdiff<0:
		ChainCountdiffc="neg_numeric"
	elif ChainCountdiff>0:
		ChainCountdiffc="pos_numeric"
	else:
		ChainCountdiffc="zero_numeric"
	ChainHasUniprotdiff=ChainHasUniprot-atoi(prev_dat['ChainHasUniprot'])
	if ChainHasUniprotdiff<0:
		ChainHasUniprotdiffc="neg_numeric"
	elif ChainHasUniprotdiff>0:
		ChainHasUniprotdiffc="pos_numeric"
	else:
		ChainHasUniprotdiffc="zero_numeric"
	ChainHasUniprotpdiff=ChainHasUniprotp-atof(prev_dat['ChainHasUniprotp'])
	ChainHas10H50Pdiff=ChainHas10H50P-atoi(prev_dat['ChainHas10H50P'])
	if ChainHas10H50Pdiff<0:
		ChainHas10H50Pdiffc="neg_numeric"
	elif ChainHas10H50Pdiff>0:
		ChainHas10H50Pdiffc="pos_numeric"
	else:
		ChainHas10H50Pdiffc="zero_numeric"
	ChainHas10H50Ppdiff=ChainHas10H50Pp-atof(prev_dat['ChainHas10H50Pp'])
	ChainHas10H60Pdiff=ChainHas10H60P-atoi(prev_dat['ChainHas10H60P'])
	if ChainHas10H60Pdiff<0:
		ChainHas10H60Pdiffc="neg_numeric"
	elif ChainHas10H60Pdiff>0:
		ChainHas10H60Pdiffc="pos_numeric"
	else:
		ChainHas10H60Pdiffc="zero_numeric"
	ChainHas10H60Ppdiff=ChainHas10H60Pp-atof(prev_dat['ChainHas10H60Pp'])
	ChainHas30H60Pdiff=ChainHas30H60P-atoi(prev_dat['ChainHas30H60P'])
	if ChainHas30H60Pdiff<0:
		ChainHas30H60Pdiffc="neg_numeric"
	elif ChainHas30H60Pdiff>0:
		ChainHas30H60Pdiffc="pos_numeric"
	else:
		ChainHas30H60Pdiffc="zero_numeric"
	ChainHas30H60Ppdiff=ChainHas30H60Pp-atof(prev_dat['ChainHas30H60Pp'])
	ChainHas50H60Pdiff=ChainHas50H60P-atoi(prev_dat['ChainHas50H60P'])
	if ChainHas50H60Pdiff<0:
		ChainHas50H60Pdiffc="neg_numeric"
	elif ChainHas50H60Pdiff>0:
		ChainHas50H60Pdiffc="pos_numeric"
	else:
		ChainHas50H60Pdiffc="zero_numeric"
	ChainHas50H60Ppdiff=ChainHas50H60Pp-atof(prev_dat['ChainHas50H60Pp'])
	fo.write("\t<h2>Chain and homolog statistics</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><td class=\"text\">Total number of chains in EPPIC db</td><td class=\"numeric\">%.0f</td><td></td><td class=\"%s\">[%d]</td></tr>\n"%(ChainCount,ChainCountdiffc,ChainCountdiff))
	fo.write("\t<tr><td class=\"text\">Total number of chains with UniProt match</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(ChainHasUniprot,ChainHasUniprotp,ChainHasUniprotdiffc,ChainHasUniprotdiff,round(ChainHasUniprotpdiff,4)))
	fo.write("\t<tr><td class=\"text\">Total number of chains having at least 10 homologs with 50%% sequence identity</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(ChainHas10H50P,ChainHas10H50Pp,ChainHas10H50Pdiffc,ChainHas10H50Pdiff,round(ChainHas10H50Ppdiff,4)))
	fo.write("\t<tr><td class=\"text\">Total number of chains having at least 10 homologs with 60%% sequence identity</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(ChainHas10H60P,ChainHas10H60Pp,ChainHas10H60Pdiffc,ChainHas10H60Pdiff,round(ChainHas10H60Ppdiff,4)))
	fo.write("\t<tr><td class=\"text\">Total number of chains having at least 30 homologs with 60%% sequence identity</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(ChainHas30H60P,ChainHas30H60Pp,ChainHas30H60Pdiffc,ChainHas30H60Pdiff,round(ChainHas30H60Ppdiff,4)))
	fo.write("\t<tr><td class=\"text\">Total number of chains having at least 50 homologs with 60%% sequence identity</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(ChainHas50H60P,ChainHas50H60Pp,ChainHas50H60Pdiffc,ChainHas50H60Pdiff,round(ChainHas50H60Ppdiff,4)))
	fo.write("\t</table>\n")
#	fo.write("\t<h2>Taxonomic distribution in EPPIC db</h2>\n")
#        fo.write("\t<table>\n")
        #fo.write("\t<tr><td><b>Taxonomy</b></td><td><b>No. of chains</b></td></tr>\n")
#        for ent in Taxonomy:
#                val=ent.split("\t")
#                fo.write("\t<tr><td>%s</td><td>%.0f</td><td>(%.2f %%)</td></tr>\n"%(val[0],atof(val[1]),100*(atof(val[1])/ChainHasUniprot)))
#        fo.write("\t</table>\n")
	
	fo.write("\t<h2>Interface area statistics (Top 10)</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><th>PDBId</th><th>Exp.method</th><th class=\"numeric\">InterfaceId</th><th class=\"numeric\">Interface area</th></tr>\n")
	for ent in Top10Area:
		val=ent.split("\t")
		fo.write("\t<tr><td class=\"text\"><a href=\"http://www.eppic-web.org/ewui/#id/%s\" onclick=\"reloadPage('http://www.eppic-web.org/ewui/#id/%s');\">%s</a></td><td class=\"text\">%s</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">%0.2f &Aring;<sup>2</sup></td></tr>\n"%(val[0],val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	fo.write("\t</table>\n")

	fo.write("\t<h2>Core residues statistics (Top 10)</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><th>PDBId</th><th>Exp.method</th><th class=\"numeric\">InterfaceId</th><th class=\"numeric\">Total no. of core residues</th></tr>\n")
	for ent in Top10Core:
		val=ent.split("\t")
		fo.write("\t<tr><td class=\"text\"><a href=\"http://www.eppic-web.org/ewui/#id/%s\" onclick=\"reloadPage('http://www.eppic-web.org/ewui/#id/%s');\">%s</a></td><td class=\"text\">%s</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">%.0f</td></tr>\n"%(val[0],val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	fo.write("\t</table>\n")

	fo.write("\t<h2>Maximum number of interfaces in a single PDB entry (Top 10)</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><th>PDBId</th><th>Exp.method</th><th class=\"numeric\">Total no. of Interfaces</th></tr>\n")
	for ent in Top10inter:
		val=ent.split("\t")
		fo.write("\t<tr><td class=\"text\"><a href=\"http://www.eppic-web.org/ewui/#id/%s\" onclick=\"reloadPage('http://www.eppic-web.org/ewui/#id/%s');\">%s</a></td><td class=\"text\">%s</td><td class=\"numeric\">%.0f</td></tr>\n"%(val[0],val[0],val[0],val[1],atof(val[2])))
	fo.write("\t</table>\n")
	

	fo.write("\t<h2>Largest interface clusters in a single PDB entry (Top 10)</h2>\n")
        fo.write("\t<table>\n")
        fo.write("\t<tr><th>PDBId</th><th>Exp.method</th><th class=\"numeric\">ClusterId</th><th class=\"numeric\">Cluster size</th></tr>\n")
        for ent in Top10Clusters:
                val=ent.split("\t")
                fo.write("\t<tr><td class=\"text\"><a href=\"http://www.eppic-web.org/ewui/#id/%s\" onclick=\"reloadPage('http://www.eppic-web.org/ewui/#id/%s');\">%s</a></td><td class=\"text\">%s</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">%.0f</td></tr>\n"%(val[0],val[0],val[0],val[1],atof(val[2]),atof(val[3])))
        fo.write("\t</table>\n")

	fo.write("\t<h2>Highly conserved interfaces based on Eppic evolutionary score (Top 10)</h2>\n")
	fo.write("\t<table>\n")
	fo.write("\t<tr><th>PDBId</th><th>Exp.method</th><th class=\"numeric\">InterfaceId</th><th class=\"numeric\">Core-surface score</th></tr>\n")
	for ent in Top10eppic:
		val=ent.split("\t")
		fo.write("\t<tr><td class=\"text\"><a href=\"http://www.eppic-web.org/ewui/#id/%s\" onclick=\"reloadPage('http://www.eppic-web.org/ewui/#id/%s');\">%s</a></td><td class=\"text\">%s</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">%0.2f</td></tr>\n"%(val[0],val[0],val[0],val[1],atof(val[2]),atof(val[3])))
	fo.write("\t</table>\n")

	fo.write("\t<h2>Experimental technique statistics</h2>\n")
	fo.write("\t<table>\n")
	for ent in ExpStat:
		val=ent.split("\t")
		diffvalue=atof(val[1])-atoi(prev_dat[val[0]])
		diffper=((atof(prev_dat[val[0]])/atof(prev_dat["EppicCount"]))*100)-((atof(val[1])/EppicCount)*100)
		if diffvalue<0:
			diffc="neg_numeric"
		elif diffvalue>0:
			diffc="pos_numeric"
		else:
			diffc="zero_numeric"
		fo.write("\t<tr><td class=\"text\">%s</td><td class=\"numeric\">%.0f</td><td class=\"numeric\">(%0.2f %%)</td><td class=\"%s\">[%d (%0.4f %%)]</td></tr>\n"%(val[0],atof(val[1]),(atof(val[1])/EppicCount)*100,diffc,diffvalue,round(diffper,4)))
	fo.write("\t</table>\n")
	fo.write("\t<h3>For the RCSB PDB statistics page, click <a href=\"http://www.pdb.org/pdb/static.do?p=general_information/pdb_statistics/index.html\" target=\"_blank\">here</a></h3>\n")
	fo.write("</div>\n")
	fo.write("</div>\n")
	fo.write("</body>\n</html>")
if __name__=="__main__":
	dbname='eppic_2014_08'
	total=365
	new=165
	removed=10
	uniprot='2014_08'
	rsyncfile='PDB-rsync_2014-09-17.log'
	get_stat(dbname,total,new,removed,uniprot,rsyncfile)	

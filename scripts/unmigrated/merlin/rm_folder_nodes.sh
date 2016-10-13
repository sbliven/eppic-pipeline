#!/bin/bash

#--------------------------------------------------
# Author : Kumaran Baskaran
# Date 28.06.2013
#--------------------------------------------------
help=" Usage : $0 \n
	\t\t [-f <folder name with full path> \n
	\t\t -l <host list file>]\n
	\t Example : $0 -f /scratch/baskaran_k/uniprot_2013_04 -l ./hosts.list\n\n "
while getopts :f:l:h option
do
	case "${option}"
	in
		f) folder=${OPTARG};;
		l) hosts=${OPTARG};;
		h) echo -e $help;;
		\?) print >&2 $help
			exit 1;;
		:) echo "Option -$OPTARG requires an argument" >&2
			exit 1;;
	esac
done

if [ -z $folder ]
then 
	echo -e "\n --------SOME OPTIONS MISSING------------"
	echo -e $help
	exit 1
fi

for n in `cat $hosts`
do
	echo "Deleting $folder from $n..."
	ssh $n rm -rf $folder
done

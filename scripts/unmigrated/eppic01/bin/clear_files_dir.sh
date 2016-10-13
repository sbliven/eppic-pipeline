#!/bin/bash

#---------------------------------------------------------------------
# Script will delete *.pml, *.jmol, *.png files from given folder
#      
# Author : Kumaran Baskaran
# Date   : 09/02/2015
#
# Note : This script is based on the dir structure created by Jose and Nikhil script.
#
#
#----------------------------------------------------------------------------

help="Usage: $0 \n
        \t  [-f dir   : folder that contains *.pml,*.jmol,*.png in subfolders \n
        \t   -h help  : help ]\n
	Example: $0 -f /bigdata/files_2014_05\n"
         
while getopts :f:h option
do
        case "${option}"
        in
                f) inputfolder=${OPTARG};;
                h) echo -e $help
		   exit 0;;
               \?) echo -e $help
                   exit 1;;
                :) echo "Option -$OPTARG requires an argument." >&2
                   exit 1;;
        esac
done

if [[ -z $inputfolder ]]
then
        echo -e "\n ----SOME OPTIONS NOT SPECIFIED CORRECTLY------"
        echo -e $help
        exit 1
fi

find $inputfolder/ -name "*.gz" -exec rm -rf {} \; -name "*.jmol" -exec rm -rf {} \; -or -name "*.pml" -not -name "*.entropies.pml" -exec rm -rf {} \; -or -name "*.png" -exec rm -rf {} \;


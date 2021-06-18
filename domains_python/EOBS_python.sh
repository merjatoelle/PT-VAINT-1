#!/bin/bash

#-------------------------------------------------------------------------------
#
# Current code owner:
#
#   Center Enviroment System Research (CESR)
#
# Authors:
#
#   CESR, 2021
#   Evgenii Churiulin, Vladimir Kopeykin, Merja Toelle
#   phone:  +49 170-261-51-04
#   email:  evgenychur@uni-kassel.de
#
#-------------------------------------------------------------------------------

#source ~/.profile


#========================= Settings ============================================
# Can be changed by user

#============================ HYRAS or EOBS ====================================

dataset="EOBS"

# E-ObS parameters for analysis
parameter=("T_2M")
count=0

#============================== General settings ===============================

# The research domain
domain=("parc_domain" "linden_domain" "lindenberg_domain")
area=("parc" "linden" "lindenberg")
# Count of domain --> should be the same as domain and coordinates parameters
paramscount=2

#========================= Paths ===============================================
DIR=/work/bb1112/b381275
#========================= Generation operations ===============================


for (( i=0; i<=paramscount ; i++ ));
do

    # Folders for EOBS input data
    DIR_IN=${DIR}/${dataset}/"${domain[${i}]}"

    # Folders for EOBS otput data
    DIR_OUT=${DIR}/results/PYTHON                     # WORK server

    # Folder for EOBS data
    DIR_RESULT=/pf/b/b381275/COSMO_results/PYTHON/    # PF server

    for (( j=0; j<=count ; j++ ));
    do
        # Input EOBS file (result EOBS_domain.sh)
        iEOBS="${DIR_IN}"/"${dataset}"_"${domain[${i}]}"."nc"

        # Output EOBS file
        oEOBS="${DIR_OUT}"/"${dataset}"_"${parameter[${j}]}"_"${area[${i}]}"."nc"

        # Get EOBS mean values
        cdo fldmean "${iEOBS}" "${oEOBS}"

        # Get EOBS csv values
        cdo outputts "${oEOBS}" > ${DIR_OUT}/"${dataset}"_"${parameter[${j}]}"_"${area[${i}]}"_"mean"."csv"

        # Copy data
        cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}

    done
done
rm -r ${DIR_OUT}/*



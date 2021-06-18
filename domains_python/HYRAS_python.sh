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

dataset="HYRAS"

# The names of folder for HYRAS parameters
param_2=("T_2M" "T_MAX" "T_MIN" "PREC")
count=3


#============================== General settings ===============================

# The research domain
domain=("parc_domain" "linden_domain" "lindenberg_domain")

# The research territory
area=("parc" "linden" "lindenberg")
# Count of domain --> should be the same as domain and coordinates parameters
paramscount=2



#========================= Paths ===============================================
DIR=/work/bb1112/b381275


#========================= Generation operations ===============================


for (( i=0; i<=paramscount ; i++ ));
do
    # Output path for HYRAS data
    DIR_OUT=${DIR}/results/PYTHON                      # WORK server
    DIR_RESULT=/pf/b/b381275/COSMO_results/PYTHON/     # PF server

    for (( j=0; j<=count ; j++ ));
    do
        # Folders for HYRAS input data
        DIR_IN=${DIR}/${dataset}/"${param_2[${j}]}"/"${domain[${i}]}"

        # Input HYRAS data (result of HYRAS_domain.sh)
        iHYRAS="${DIR_IN}"/"${dataset}"_"${param_2[${j}]}"_"${domain[${i}]}".nc

        # Output HYRAS data (for python)
        oHYRAS="${DIR_OUT}"/"${dataset}"_"${param_2[${j}]}"_"${area[${i}]}"."nc"

        # Get mean HYRAS values
        cdo fldmean "${iHYRAS}" "${oHYRAS}"

        # Get HYRAS csv
        cdo outputts "${oHYRAS}" > ${DIR_OUT}/"${dataset}"_"${param_2[${j}]}"_"${area[${i}]}"_"mean"."csv"

        # Copy to PF server
        cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}
    done
done
rm -r ${DIR_OUT}/*



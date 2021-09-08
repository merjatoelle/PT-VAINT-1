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

dataset="GLEAM"

# Format of GLEAM data
type_GLEAM="v3.5a"
#type_GLEAM="v3.5b"

# General filename for GLEAM dataset
filename="GLEAM_2010_2015"         # GLEAM dataset

if [ "${type_GLEAM}" == "v3.5a" ]; then
    param=("E" "Ei" "Ep" "Es" "Et")        # GLEAM parameters
    gleamcount=4
else
    param=("E" "Ep" "Es" "Et")
    gleamcount=3
fi


#============================== General settings ===============================

# The research domain
domain=("parc_domain" "linden_domain" "lindenberg_domain")
area=("parc" "linden" "lindenberg")
# Count of domain --> should be the same as domain and coordinates parameters
paramscount=2


#========================= Paths ===============================================
DIR=/work/bb1112/b381275


#========================= Generation operations ===============================

# Cycle for GLEAM parameters
for (( i=0; i<=paramscount ; i++ ));
do
    DIR_IN=${DIR}/${dataset}/${type_GLEAM}/"${domain[${i}]}"
    DIR_OUT=${DIR}/results/PYTHON
    DIR_RESULT=/pf/b/b381275/COSMO_results/PYTHON/

    for (( j=0; j<=gleamcount ; j++ ));
    do
        # Input GLEAM data (result of GLEAM.sh)
        iGLEAM="${DIR_IN}"/"${param[${j}]}"_"${filename}".nc

        # Output GLEAM data (for python)
        oGLEAM="${DIR_OUT}"/"${dataset}"_"${param[${j}]}"_"${area[${i}]}"."nc"

        # Get mean GLEAM values
        cdo fldmean "${iGLEAM}" "${oGLEAM}"

        # Get GLEAM csv
        cdo outputts "${oGLEAM}" > ${DIR_OUT}/"${param[${j}]}"_"${dataset}"_"${type_GLEAM}"_"${area[${i}]}"_"mean"."csv"

        # Copy to COSMO_reults
        cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}
    done
done
rm -r ${DIR_OUT}/*



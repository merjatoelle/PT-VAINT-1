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


if [ "${type_GLEAM}" == "v3.5a" ]; then
    # The name of dataset
    ifilename="GLEAM_1999_2020"         # GLEAM dataset
    ofilename="GLEAM_2010_2015"         # GLEAM dataset
    param=("E" "Ei" "Ep" "Es" "Et")        # GLEAM parameters
    gleamcount=4
else
    # The name of dataset
    ifilename="GLEAM_2003_2020"         # GLEAM dataset
    ofilename="GLEAM_2010_2015"         # GLEAM dataset
    param=("E" "Ep" "Es" "Et")
    gleamcount=3
fi


#============================== General settings ===============================

# The research domain
domain=("parc_domain" "linden_domain" "lindenberg_domain")
area=("parc.nc" "linden.nc" "lindenberg.nc")
paramscount=2

#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_DATA=${DIR}/${dataset}/DATA/${type_GLEAM}
#========================= Generation operations ===============================

# Cycle for GLEAM parameters
for (( i=0; i<=paramscount ; i++ ));
do
    DIR_OUT=${DIR}/${dataset}/${type_GLEAM}/"${domain[${i}]}"

    for (( j=0; j<=gleamcount ; j++ ));
    do
        # Input GLEAM data
        iGLEAM="${DIR_DATA}"/"${param[${j}]}"_"${ifilename}"_"${area[${i}]}"
        # Output GLEAM data
        oGLEAM="${DIR_OUT}"/"${param[${j}]}"_"${ofilename}".nc

        cdo seldate,20100101,20153112 "${iGLEAM}" "${oGLEAM}"
    done
done

echo 'All done_'$type_GLEAM







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

#============================ EOBS =============================================

dataset="EOBS"

# The name of dataset
ifilename="tg_0.22deg_rot_v12.0.nc"         #  EOBS dataset
ofilename="tas_eobs_5_2010_2015.nc"

#============================== General settings ===============================

# The research domain
domain=("parc_domain" "linden_domain" "lindenberg_domain")
grid=("grid_parc.txt" "grid_linden.txt" "grid_lindenberg.txt")
# Count of domain --> should be the same as domain and coordinates parameters
paramscount=2


#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_DATA=${DIR}/${dataset}/DATA

#========================= Generation operations ===============================

ieobs="${DIR_DATA}"/"${ifilename}"
oeobs="${DIR_DATA}"/"${ofilename}"

# Extract time period from 01.01.2010 to 30.06.2015
cdo seldate,20100101,20153112 "${ieobs}" "${oeobs}"

for (( i=0; i<=paramscount ; i++ ));
do
    # Folders EOBS output data
    DIR_RESULT=${DIR}/${dataset}/"${domain[${i}]}"

    # Domain grid
    mygrid=${DIR_DATA}/"${grid[${i}]}"

    # Input EOBS file
    ifile="${DIR_DATA}"/"${ofilename}"
    #Output HYRAS or EOBS file
    ofile="${DIR_RESULT}"/"${dataset}"_"${domain[${i}]}".nc

    # Interpolation EOBS data to COSMO grid
    cdo remapbil,"${mygrid}" "${ifile}" "${ofile}"

done

echo 'All done EOBS'




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

# The names of HYRAS parameters (datasets)
param_1=("tas" "tmax" "tmin" "pres")

# The names of folder for HYRAS parameters
param_2=("T_2M" "T_MAX" "T_MIN" "PREC")
count=3


# The name of dataset - general for all data
filename="hyras_5_2010_2015.nc"



#============================== General settings ===============================

# The research domain
domain=("parc_domain" "linden_domain" "lindenberg_domain")

# The grids for interpolation
grid=("grid_parc.txt" "grid_linden.txt" "grid_lindenberg.txt")

# Count of domain --> should be the same as domain and coordinates parameters
paramscount=2


#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_IN=${DIR}/${dataset}/DATA

#========================= Generation operations ===============================

for (( i=0; i<=paramscount ; i++ ));
do

    for (( j=0; j<=count ; j++ ));
    do
        # Domain grid --> grid for interpolation
        mygrid=${DIR_IN}/"${grid[${i}]}"

        # Input HYRAS file
        iHYRAS="${DIR_IN}"/"${param_1[${j}]}"_"${filename}"

        # Folders for HYRAS output data
        DIR_OUT=${DIR}/${dataset}/"${param_2[${j}]}"/"${domain[${i}]}"

        #Output HYRAS or EOBS file
        oHYRAS="${DIR_OUT}"/"${dataset}"_"${param_2[${j}]}"_"${domain[${i}]}".nc

        cdo remapbil,"${mygrid}" "${iHYRAS}" "${oHYRAS}"

    done
done

echo 'All done HYRAS'

#echo 'test'$DIR_RESULT



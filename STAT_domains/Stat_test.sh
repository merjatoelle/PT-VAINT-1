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

#=============================== HYRAS =========================================

refer="HYRAS"

# The HYRAS parameters for analysis
param_HYRAS=("T_2M" "T_MAX" "T_MIN" "T_2M")

# The COSMO parameters for analysis
param_COSMO=("T_2M" "TMAX_2M" "TMIN_2M" "T_S")

# Count of parameters --> should be the same as param_HYRAS and param_COSMO
paramscount=3

# The research domain
#domain=("parc_domain" "linden_domain" "lindenberg_domain")
domain=("lindenberg_domain")
# Count of domain
domaincount=0
#============================== General settings ===============================

# The name of dataset: ds_1 - COSMO ORIGINAL
#                      ds_2 - COSMO v3.5 (b =  2000)
#                      ds_3 - COSMO v4.5 (b = 10000)
#                      ds_4 - COSMO v4.5 with changes in ztraleav
dataset="ds_1"

# Use dataset
if [ "${dataset}" == "ds_1" ]; then
    ds_folder="original"
    ds_name="COSMO_ORIG"

elif [ "${dataset}" == "ds_2" ]; then
    ds_folder="3.5"
    ds_name="COSMO_35"

elif [ "${dataset}" == "ds_3" ]; then
    ds_folder="4.5"
    ds_name="COSMO_45"

elif [ "${dataset}" == "ds_4" ]; then
    ds_folder="4.5e"
    ds_name="COSMO_45e"

else
    echo 'no datasets'
fi


#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_OUT=${DIR}/results/${refer}                                                 # Output path at WORK server of mistral
DIR_RESULT=/pf/b/b381275/COSMO_results/${refer}                                 # output path at PF   server of mistral

#========================= Generation operations ===============================

for (( i=0; i<=domaincount ; i++ ));
do

    for (( j=0; j<=paramscount ; j++ ));
    do
        #-----------------------------------------------------------------------
        # Define input and output HYRAS data
        #-----------------------------------------------------------------------

        # Input path for HYRAS data
        DIR_HYRAS=${DIR}/${refer}

        # Filename of observational dataset: HYRAS
        refer_fn="${refer}"_"${param_HYRAS[${j}]}"_"${domain[${i}]}".nc

        # Input and Output data:
        iHYRAS=${DIR_HYRAS}/"${refer_fn}"
        sHYRAS=${DIR_OUT}/"${refer}"_"${param_HYRAS[${j}]}"_"std"_"${domain[${i}]}"
        mHYRAS=${DIR_OUT}/"${refer}"_"${param_HYRAS[${j}]}"_"mean"_"${domain[${i}]}"
        dHYRAS=${DIR_OUT}/"${refer}"_"${param_HYRAS[${j}]}"_"mean_dav"_"${domain[${i}]}"
        #-----------------------------------------------------------------------
        # Define input and output COSMO data
        #-----------------------------------------------------------------------

        # Input paths for COSMO data
        DIR_COSMO=${DIR}/COSMO/"${domain[${i}]}"/"${ds_folder}"

        # Filename of model dataset: COSMO_ORIG, COSMO_v35, COSMO_v45, COSMO_v45e
        #model_ds="${param_COSMO[${j}]}"_"ts_1999_2015.nc"
        model_ds="${param_COSMO[${j}]}"_"ts_1999_2015.nc"
        # Paths for semiresults
        iCOSMO=${DIR_COSMO}/"${model_ds}"
        oCOSMO=${DIR_OUT}/"${ds_name}"_"${param_COSMO[${j}]}"_"daily.nc"

        # Paths for COSMO mean data and std data
        sCOSMO=${DIR_OUT}/"${ds_name}"_"${param_COSMO[${j}]}"_"std"             #  STD COSMO
        mCOSMO=${DIR_OUT}/"${ds_name}"_"${param_COSMO[${j}]}"_"mean"            # Mean COSMO

        if [ "${param_COSMO[${j}]}" == "T_S" ] ; then
            so_COSMO=${DIR_OUT}/"${ds_name}"_"${param_COSMO[${j}]}"_"std"_"${domain[${i}]}"                                         # For COSMO STD
            mo_COSMO=${DIR_OUT}/"${ds_name}"_"${param_COSMO[${j}]}"_"mean"_"${domain[${i}]}"                                        # For COSMO MEAN
            da_COSMO=${DIR_OUT}/"${ds_name}"_"${param_COSMO[${j}]}"_"mean_dav"_"${domain[${i}]}"                                    # For COSMO MEAN DAV
            o_CORR=${DIR_OUT}/"Corr"_"${refer}"_"${ds_name}"_"${param_COSMO[${j}]}"_"${domain[${i}]}"                               # For CORR
        else
            so_COSMO=${DIR_OUT}/"${ds_name}"_"${param_HYRAS[${j}]}"_"std"_"${domain[${i}]}"
            mo_COSMO=${DIR_OUT}/"${ds_name}"_"${param_HYRAS[${j}]}"_"mean"_"${domain[${i}]}"
            da_COSMO=${DIR_OUT}/"${ds_name}"_"${param_HYRAS[${j}]}"_"mean_dav"_"${domain[${i}]}"
            o_CORR=${DIR_OUT}/"Corr"_"${refer}"_"${ds_name}"_"${param_HYRAS[${j}]}"_"${domain[${i}]}"
        fi

        #-----------------------------------------------------------------------
        # Calculations for KGE and RMSD
        #-----------------------------------------------------------------------

        # Convert MODEL data to HYRAS format
        cdo -daymean -subc,273.15 "${iCOSMO}" "${oCOSMO}"

        # Calcuate standart deviation (std) and mean for MODEL
        cdo timstd "${oCOSMO}" "${sCOSMO}"."nc"
        cdo timmean "${oCOSMO}" "${mCOSMO}"."nc"

        # Calcuate standart deviation (std) and mean for HYRAS
        cdo timstd "${iHYRAS}" "${sHYRAS}"."nc"
        cdo timmean "${iHYRAS}" "${mHYRAS}"."nc"

        #Calculation of correlation between reference and dataset
        #if [  ]; then

        #else
            #statements
        #fi
        cdo timcor "${iHYRAS}" "${oCOSMO}" "${o_CORR}"."nc"
        #cdo fldcor "${iHYRAS}" "${oCOSMO}" "${o_CORR}"."nc"
        #-----------------------------------------------------------------------

        # Output NetCDF > csv for MODEL dataset
        cdo -outputtab,date,lon,lat,value "${sCOSMO}"."nc" > "${so_COSMO}"."csv"
        cdo -outputtab,date,lon,lat,value "${mCOSMO}"."nc" > "${mo_COSMO}"."csv"

        # Output NetCDF > csv for HYRAS dataset
        cdo -outputtab,date,lon,lat,value "${sHYRAS}"."nc" > "${sHYRAS}"."csv"
        cdo -outputtab,date,lon,lat,value "${mHYRAS}"."nc" > "${mHYRAS}"."csv"

        # Output NetCDF > csv for correletion
        cdo -outputtab,date,lon,lat,value "${o_CORR}"."nc" > "${o_CORR}"."csv"

        #-----------------------------------------------------------------------
        # Calculations for DAV
        #-----------------------------------------------------------------------
        # Calculate std, mean for HYRAS dataset
        cdo fldmean "${iHYRAS}" "${dHYRAS}"."nc"
        # Calculate std, mean for MODEL dataset
        cdo fldmean "${oCOSMO}" "${da_COSMO}"."nc"
        #-----------------------------------------------------------------------
        # Output NetCDF > csv for HYRAS dataset
        cdo -outputts "${dHYRAS}"."nc" > "${dHYRAS}"."csv"
        # Output NetCDF > csv for MODEL dataset
        cdo -outputts "${da_COSMO}"."nc" > "${da_COSMO}"."csv"

    done
done

cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}
rm -r ${DIR_OUT}/*




        #cdo fldstd "${i_hyras_data}" "${s_hyras_data}"."nc"
        #cdo fldmean "${i_hyras_data}" "${m_hyras_data}"."nc"
        #cdo fldstd "${oCOSMO_s1}" "${s_cosmo_data}"."nc"
        #cdo fldmean "${oCOSMO_s1}" "${m_cosmo_data}"."nc"


        # Convert from NetCDF format > csv format for model dataset
        #cdo outputts "${s_cosmo_data}"."nc" > "${s_output_cosmo}"."csv"
        #cdo outputts "${m_cosmo_data}"."nc" > "${m_output_cosmo}"."csv"

                # NetCDF > csv for observations
        #cdo outputts "${s_hyras_data}"."nc" > "${s_hyras_data}"."csv"
        #cdo outputts "${m_hyras_data}"."nc" > "${m_hyras_data}"."csv"

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

# The research domain
#domain=("parc_domain" "linden_domain" "lindenberg_domain")
domain=("parc_domain")
# Count of domain --> should be the same as domain and coordinates parameters
domaincount=0


# The HYRAS parameters for analysis
params=("T_2M")
paramscount=0




#============================== General settings ===============================









# The name of dataset: ds_1 - COSMO ORIGINAL
#                      ds_2 - COSMO v3.5 (b =  2000)
#                      ds_3 - COSMO v4.5 (b = 10000)
#                      ds_4 - COSMO v4.5 with changes in ztraleav
dataset="ds_4"



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




DIR_OUT_TEST=/work/bb1112/b381275/results/TEST
DIR_IN_TEST=/work/bb1112/b381275/HYRAS/parc_domain
cdo remapbil,mygrid ${DIR_IN_TEST}/"HYRAS_parc_domain"."nc" ${DIR_OUT_TEST}/"RM_data"."nc"


#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_OUT=${DIR}/results/ANALYSIS
#DIR_RESULT=/pf/b/b381275/COSMO_results/ANALYSIS

#========================= Generation operations ===============================

for (( i=0; i<=domaincount ; i++ ));
do
    # Input path for HYRAS data
    DIR_HYRAS_IN=${DIR}/${refer}/"${domain[${i}]}"
    # Filename of observational dataset: HYRAS
    refer_fn="${refer}"_"${domain[${i}]}".nc

    # Input paths for COSMO data
    DIR_IN_COSMO=${DIR}/COSMO/"${domain[${i}]}"

    # Output paths at WORK server of mistral
    DIR_OUT=${DIR}/results/${refer}/"${domain[${i}]}"
    # Output paths in PF server of mistral (final path)
    DIR_RESULT=/pf/b/b381275/COSMO_results/${refer}/"${domain[${i}]}"/${ds_folder}


    for (( j=0; j<=paramscount ; j++ ));
    do
        # Filename of model dataset: COSMO_ORIG, COSMO_v35, COSMO_v45, COSMO_v45e
        model_ds="${params[${j}]}"_"ts_1999_2015.nc"


        #-----------------------------------------------------------------------
        # Preparing COSMO data
        #-----------------------------------------------------------------------

        # Convert from 1 hour timestep to daily values
        cdo daymean ${DIR_IN_COSMO}/"${ds_folder}"/"${model_ds}" ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"daily"."nc"


        # Set time
        cdo settime,00:00, ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"daily"."nc" ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"final"."nc"

        if [ "${params[${j}]}" == "T_2M" ]; then
            cdo expr,'var2=T_2M-273.15;' ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"final"."nc" ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean_daily"."nc"
        else
            echo 'I do not use convertation from K to C'
        fi


        # Calcuate standart deviation (std) for model dataset
        #-----------------------------------------------------------------------
        cdo fldstd ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean_daily"."nc" ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"std"."nc"

        # Convert from NetCDF format > csv format for model dataset
        cdo outputts ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"std"."nc" > ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"std_daily"."csv"
        #cdo -outputtab,date,lon,lat,value ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"std"."nc" > ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"std_daily"."csv"
        #-----------------------------------------------------------------------


        # Calcuate mean values (mean) for model dataset
        #-----------------------------------------------------------------------
        cdo fldmean ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean_daily"."nc" ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean"."nc"

        # Convert from NetCDF format > csv format for model dataset
        cdo outputts ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean"."nc" > ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean_daily"."csv"
        #-----------------------------------------------------------------------



        # Calculation of statistic for observations (HYRAS, E-OBS, GLEAM)
        #-----------------------------------------------------------------------

        # Calcuate standart deviation (std) for observation dataset
        #-----------------------------------------------------------------------
        cdo fldstd ${DIR_IN_DATASET}/"${refer_data}" ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"std"."nc"
        # NetCDF > csv for model dataset
        cdo outputts ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"std"."nc" > ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"std"."csv"

        # Calcuate mean values (mean) for observation dataset
        #-----------------------------------------------------------------------
        cdo fldmean ${DIR_IN_DATASET}/"${refer_data}" ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"mean"."nc"

        cdo outputts ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"mean"."nc" > ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"mean"."csv"



        #cdo timmean ${DIR_OUT_TEST}/"RM_data"."nc" ${DIR_OUT_TEST}/"RM_data"_"mean"."nc"
        #cdo -outputtab,date,lon,lat,value ${DIR_OUT_TEST}/"RM_data"_"mean"."nc" > ${DIR_OUT_TEST}/"RM_data"_"mean"."csv"



        # Calculation of correlation between reference and dataset
        #-----------------------------------------------------------------------
        #cdo fldcor -setmissval,-9e33 ${DIR_OUT}/"HYRAS"_"${params[${j}]}"_"mean_obs"."nc" -setmissval,-9e33 ${DIR_OUT}/"${ds_name}"_"${model_ds}"_"mean_mod"."nc" ${DIR_OUT}/"Corr_HYRAS"_"${ds_name}"_"${params[${j}]}"."nc"

        cdo timcor ${DIR_OUT}/"${refer}"_"${params[${j}]}"_"mean"."nc" ${DIR_OUT}/"${ds_name}"_"${params[${j}]}"_"mean"."nc" ${DIR_OUT}/"Corr"_"${refer}"_"${ds_name}"_"${params[${j}]}"."nc"

        cdo outputts ${DIR_OUT}/"Corr"_"${refer}"_"${ds_name}"_"${params[${j}]}"."nc" > ${DIR_OUT}/"Corr"_"${refer}"_"${ds_name}"_"${params[${j}]}"."csv"



    done

done


cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}
rm -r ${DIR_OUT}/*
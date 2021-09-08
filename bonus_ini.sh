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

# possible options: 1 - Parc; 2 - Linden; 3 - Lindenberg
mode="3"

# possible versions: 3.5; 4.5; 4.5e
exp_version=("3.5" "4.5" "4.5e")
ver_count=2

params=("ZEP_S_ts"   "ZDQS_S_ts"  "RSTOM_SUN_ts" "RSTOM_SHA_ts" "CONDUCT_ts" \
        "LAI_SUN_ts" "LAI_SHA_ts" "PAR_SUN_ts"   "PAR_SHA_ts"   "COSZ_ts"    \
        "SLA_SUN_ts" "SLA_SHA_ts" "RBST_ts"      "EAH_ts"     "DAYLENTGH_ts" \
        "PSN_ts"     "VC_SUN_ts"  "VC_SHA_ts"                                )

paramscount=17

fn_name="1999_2015"

fn_research="2010_2015"

#========================= Paths ===============================================
# Upload correct filenames
if [ "${mode}" == "1" ]; then
    version="Parc"
    domain="parc_domain"
    f_out="PARC"

elif [ "${mode}" == "2" ]; then
    version="Linden"
    domain="linden_domain"
    f_out="LINDEN"

elif [ "${mode}" == "3" ]; then
    version="Lindenberg"
    domain="lindenberg_domain"
    f_out="LINDENBERG"
else
    echo 'No data for analysis'
fi

for (( i=0; i<=ver_count ; i++ ));
do
    echo 'The experiment version: '${exp_version[${i}]}
    echo 'The research territory: '$f_out


    DIR=/work/bb1112/b381275
    if [ "${exp_version[${i}]}" == "4.5e" ]; then
        DIR_COSMO_DATA=${DIR}/"${version}"_v4.5_evap/post
        #echo 'path: '$DIR_COSMO_DATA
    else
        DIR_COSMO_DATA=${DIR}/"${version}"_v"${exp_version[${i}]}"/post
    fi
    DIR_OUT=${DIR}/results/COSMO_exp/"${f_out}"_v"${exp_version[${i}]}"
    DIR_RESULT=/pf/b/b381275/COSMO_results/"${f_out}"/v"${exp_version[${i}]}"
    #========================= Generation operations ===============================

    for (( j=0; j<=paramscount ; j++ ));
    do
        echo ' Actual parameter is: '${params[${j}]}
        # The name of COSMO-CLM parameter for analysis
        fn_COSMO=${params[${j}]}."nc"
        # The paths to COSMO-CLM data (control run)
        ts_COSMO="${DIR_COSMO_DATA}"/*/"${fn_COSMO}"

        # The full timeseries with COSMO data from 1999 to 2020
        fCOSMO=${DIR_OUT}/"${params[${j}]}"_"${fn_name}"
        # The research timeseries with COSMO data from 2010 to 2015
        rCOSMO=${DIR_OUT}/"${params[${j}]}"_"${fn_research}"
        # Path to result
        res_COSMO=${DIR_OUT}/"${params[${j}]}"_"mean"_"${fn_name}"

        # Main calculations
        ncrcat -h ${ts_COSMO} "${fCOSMO}"."nc"
        cdo seldate,20100101,20153112 "${fCOSMO}"."nc" "${rCOSMO}"."nc"
        cdo fldmean "${rCOSMO}"."nc" "${res_COSMO}"."nc"
        cdo outputts "${res_COSMO}"."nc" > "${res_COSMO}"."csv"

    done
    cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}
    rm -r ${DIR_OUT}/*
done
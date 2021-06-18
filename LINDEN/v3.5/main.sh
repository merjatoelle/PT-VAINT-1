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
params=("AEVAP_S_ts"   "ALHFL_S_ts" "ALHFL_BS_ts" "ALHFL_PL_ts" "ASHFL_S_ts" \
          "QV_2M_ts"      "QV_S_ts"     "T_2M_ts"  "TMAX_2M_ts" "TMIN_2M_ts" \
            "T_S_ts" "RELHUM_2M_ts"    "RSTOM_ts" "ZTRALEAV_ts"  "ZTRANG_ts" \
        "ZTRANGS_ts"    "ZVERBO_ts"       "PS_ts"                            )

paramscount=17

fn_name="1999_2015"
#echo $time_step
fn_research="2010_2015"

#param="AEVAP_S_ts ALHFL_S_ts ALHFL_BS_ts ALHFL_PL_ts ASHFL_S_ts QV_2M_ts QV_S_ts T_2M_ts TMAX_2M_ts TMIN_2M_ts T_S_ts RELHUM_2M_ts RSTOM_ts ZTRALEAV_ts ZTRANG_ts ZTRANGS_ts ZVERBO_ts PS_ts"

#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_COSMO_DATA=${DIR}/Linden_v3.5/post
DIR_OUT=${DIR}/results/COSMO_exp/LINDEN_v3.5
DIR_RESULT=/pf/b/b381275/COSMO_results/LINDEN/v3.5

# Additional path for COSMO field results
DIR_COSMO_RS=${DIR}/COSMO/linden_domain/3.5/
#========================= Generation operations ===============================

#for par in ${param}
#do
#    fileName_exp="${par}"."nc"
#    data_exp="${DIR_COSMO_DATA}"/*/"${fileName_exp}"



for (( j=0; j<=paramscount ; j++ ));
do
    fn_COSMO=${params[${j}]}."nc"
    # Original COSMO data for each months
    ts_COSMO="${DIR_COSMO_DATA}"/*/"${fn_COSMO}"

    # The full timeseries with COSMO data from 1999 to 2020
    fCOSMO=${DIR_OUT}/"${params[${j}]}"_"${fn_name}"
    # The research timeseries with COSMO data from 2010 to 2015
    rCOSMO=${DIR_OUT}/"${params[${j}]}"_"${fn_research}"



    # Output data from the first step
    COSMO_s1=${DIR_OUT}/"${params[${j}]}"_"vert"_"${fn_research}"
    # Second step
    COSMO_s2=${DIR_OUT}/"${params[${j}]}"_"vert_mean"_"${fn_name}"

    # Path to copy nc field to WORK server
    out_COSMO=${DIR_COSMO_RS}/
    # Path to result
    res_COSMO=${DIR_OUT}/"${params[${j}]}"_"mean"_"${fn_name}"



    # Main calculations
    ncrcat -h ${ts_COSMO} "${fCOSMO}"."nc"

    cdo seldate,20100101,20153112 "${fCOSMO}"."nc" "${rCOSMO}"."nc"


    if [ "${params[${j}]}" == "ALHFL_PL_ts" ]; then
        cdo -sellevel,1/4 "${rCOSMO}"."nc" "${COSMO_s1}"."nc"
        cdo vertsum  "${COSMO_s1}"."nc" "${COSMO_s2}"."nc"
        # Copy initial field to WORK server
        cp -R "${COSMO_s2}"."nc" "${out_COSMO}"
        # Calculations
        cdo fldmean "${COSMO_s2}"."nc" "${res_COSMO}"."nc"
        cdo outputts "${res_COSMO}"."nc" > "${res_COSMO}"."csv"

    elif [ "${params[${j}]}" == "ZTRANG_ts" ]; then
        cdo -sellevel,1/4 "${rCOSMO}"."nc" "${COSMO_s1}"."nc"
        cdo vertsum  "${COSMO_s1}"."nc" "${COSMO_s2}"."nc"
        # Copy initial field to WORK server
        cp -R "${COSMO_s2}"."nc" "${out_COSMO}"
        # Calculations
        cdo fldmean "${COSMO_s2}"."nc" "${res_COSMO}"."nc"
        cdo outputts "${res_COSMO}"."nc" > "${res_COSMO}"."csv"
    else
        # Copy initial field to WORK server
        cp -R "${rCOSMO}"."nc" "${out_COSMO}"/"${params[${j}]}"_"${fn_name}".nc
        # Calculation
        cdo fldmean "${rCOSMO}"."nc" "${res_COSMO}"."nc"
        cdo outputts "${res_COSMO}"."nc" > "${res_COSMO}"."csv"
    fi

done

cp -R ${DIR_OUT}/*."csv" ${DIR_RESULT}
rm -r ${DIR_OUT}/*
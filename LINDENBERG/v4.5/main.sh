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
param="AEVAP_S_ts ALHFL_S_ts ALHFL_BS_ts ALHFL_PL_ts ASHFL_S_ts QV_2M_ts QV_S_ts T_2M_ts TMAX_2M_ts TMIN_2M_ts T_S_ts RELHUM_2M_ts RSTOM_ts ZTRALEAV_ts ZTRANG_ts ZTRANGS_ts ZVERBO_ts PS_ts"




t_start="1999"
t_stop="2015"
format="nc"
format2="csv"

time_step="${t_start}"_"${t_stop}"."${format}"
#echo $time_step



#========================= Paths ===============================================
DIR=/work/bb1112/b381275
DIR_COSMO_EXP=${DIR}/Lindenberg_v4.5/post
DIR_RESULT=${DIR}/results/COSMO_exp/LINDENBERG_v4.5
DIR_F_RESULT=/pf/b/b381275/COSMO_results/LINDENBERG/v4.5

# Additional path for COSMO field results
DIR_COSMO_RS=${DIR}/COSMO/lindenberg_domain/4.5/

#========================= Generation operations ===============================
for param in ${param}
do
    fileName_exp="${param}"."${format}"
    data_exp="${DIR_COSMO_EXP}"/*/"${fileName_exp}"


    ncrcat -h ${data_exp} ${DIR_RESULT}/"${param}"_"${time_step}"

    if [ "${param}" == "ALHFL_PL_ts" ]; then
        cdo -sellevel,1/4 ${DIR_RESULT}/"${param}"_"${time_step}" ${DIR_RESULT}/"${param}"_"vert"_"${time_step}"

        cdo vertsum  ${DIR_RESULT}/"${param}"_"vert"_"${time_step}" ${DIR_RESULT}/"${param}"_"vert_mean"_"${time_step}"

        # Additional copy nc file for statistical analysis
        cp -R ${DIR_RESULT}/"${param}"_"vert_mean"_"${time_step}" ${DIR_COSMO_RS}

        cdo fldmean ${DIR_RESULT}/"${param}"_"vert_mean"_"${time_step}" ${DIR_RESULT}/"${param}"_"mean"_"${time_step}"

        cdo outputts ${DIR_RESULT}/"${param}"_"mean"_"${time_step}" > ${DIR_RESULT}/"${param}"_"mean"_"${t_start}"_"${t_stop}"."${format2}"

    elif [ "${param}" == "ZTRANG_ts" ]; then
        cdo -sellevel,1/4 ${DIR_RESULT}/"${param}"_"${time_step}" ${DIR_RESULT}/"${param}"_"vert"_"${time_step}"

        cdo vertsum  ${DIR_RESULT}/"${param}"_"vert"_"${time_step}" ${DIR_RESULT}/"${param}"_"vert_mean"_"${time_step}"

        # Additional copy nc file for statistical analysis
        cp -R ${DIR_RESULT}/"${param}"_"vert_mean"_"${time_step}" ${DIR_COSMO_RS}

        cdo fldmean ${DIR_RESULT}/"${param}"_"vert_mean"_"${time_step}" ${DIR_RESULT}/"${param}"_"mean"_"${time_step}"

        cdo outputts ${DIR_RESULT}/"${param}"_"mean"_"${time_step}" > ${DIR_RESULT}/"${param}"_"mean"_"${t_start}"_"${t_stop}"."${format2}"

    else
        # Additional copy nc file for statistical analysis
        cp -R ${DIR_RESULT}/"${param}"_"${time_step}" ${DIR_COSMO_RS}

        cdo fldmean ${DIR_RESULT}/"${param}"_"${time_step}" ${DIR_RESULT}/"${param}"_"mean"_"${time_step}"

        cdo outputts ${DIR_RESULT}/"${param}"_"mean"_"${time_step}" > ${DIR_RESULT}/"${param}"_"mean"_"${t_start}"_"${t_stop}"."${format2}"

    fi

    cp -R ${DIR_RESULT}/"${param}"_"mean"_"${t_start}"_"${t_stop}"."${format2}" ${DIR_F_RESULT}



done

rm -r ${DIR_RESULT}/*
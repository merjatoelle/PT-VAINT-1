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
#param="RSTOM_SUN_ts RSTOM_SHA_ts CONDUCT_ts LAI_SUN_ts LAI_SHA_ts PAR_SUN_ts PAR_SHA_ts COSZ_ts SLA_SUN_ts SLA_SHA_ts RBST_ts PSN_ts VC_SUN_ts VC_SHA_ts"
param="ZEP_S_ts ZDQS_S_ts RSTOM_SUN_ts RSTOM_SHA_ts CONDUCT_ts LAI_SUN_ts LAI_SHA_ts PAR_SUN_ts PAR_SHA_ts COSZ_ts SLA_SUN_ts SLA_SHA_ts RBST_ts EAH_ts DAYLENTGH_ts PSN_ts VC_SUN_ts VC_SHA_ts"


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

#========================= Generation operations ===============================
for param in ${param}
do
    fileName_exp="${param}"."${format}"
    data_exp="${DIR_COSMO_EXP}"/*/"${fileName_exp}"


    ncrcat -h ${data_exp} ${DIR_RESULT}/"${param}"_"${time_step}"


    cdo fldmean ${DIR_RESULT}/"${param}"_"${time_step}" ${DIR_RESULT}/"${param}"_"mean"_"${time_step}"

    cdo outputts ${DIR_RESULT}/"${param}"_"mean"_"${time_step}" > ${DIR_RESULT}/"${param}"_"mean"_"${t_start}"_"${t_stop}"."${format2}"



    cp -R ${DIR_RESULT}/"${param}"_"mean"_"${t_start}"_"${t_stop}"."${format2}" ${DIR_F_RESULT}



done

rm -r ${DIR_RESULT}/*
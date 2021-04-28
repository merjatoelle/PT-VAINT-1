# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:01:38 2021

@author: churiulin
"""

import math
import numpy as np
import pandas as pd


#------------------------------------------------------------------------------
# Subroutine: get_dav
#------------------------------------------------------------------------------
#
# The subroutine needs for getting data for DAV analisis
# 
# Input parameters : iPath   - absolute path for data
#                    ts_name - the name of parameter for analysis   
#
# Output parameters: ts      - timeseries with intersting parameter 
#
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_dav(iPath, ts_name):
    df = pd.read_csv(iPath, skiprows = 0, sep=' ', parse_dates = {'Date':[1,2]},
                     header = None)
    df = df.drop(0, axis = 1)
    # Get indices
    date_index = pd.to_datetime(df['Date'])
    # Create timeseries
    ts = pd.Series(df[3].values, index = date_index, dtype = 'float') 
    ts = ts.rename(ts_name)
    return ts

# end Subroutine get_data
#------------------------------------------------------------------------------






#------------------------------------------------------------------------------
# Subroutine: get_pdg
#------------------------------------------------------------------------------
#
# The subroutine needs for getting probability density function
# 
# Input parameters : data_array - array with data
#                    key        - the name of column for analysis   
#
# Output parameters: list_num   - probability density function  
#
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_pdf(data_array, key):
    
    df_mod = data_array
    
    count_1  = 0  # for values which are less then -10
    count_2  = 0  # for values from -10 to -5
    count_3  = 0  # for values from  -5 to  0
    count_4  = 0  # for values from   0 to  5
    count_5  = 0  # for values from   5 to 10
    count_6  = 0  # for values from  10 to 15
    count_7  = 0  # for values from  15 to 20
    count_8  = 0  # for values from  20 to 25
    count_9  = 0  # for values from  25 to 30
    count_10 = 0  # for values wich are bigger then 30
    
    for j in range(len(df_mod)):
        if df_mod[key][j] < -10.0:
            count_1 = count_1 + 1
        elif df_mod[key][j] >= -10.0 and df_mod['T_2M'][j] < -5.0:
            count_2 = count_2 + 1
        elif df_mod[key][j] >= -5.0  and df_mod['T_2M'][j] < -0.0: 
            count_3 = count_3 + 1
        elif df_mod[key][j] >=  0.0  and df_mod['T_2M'][j] <  5.0: 
            count_4 = count_4 + 1
        elif df_mod[key][j] >=  5.0  and df_mod['T_2M'][j] < 10.0: 
            count_5 = count_5 + 1
        elif df_mod[key][j] >=  10.0 and df_mod['T_2M'][j] < 15.0: 
            count_6 = count_6 + 1
        elif df_mod[key][j] >=  15.0 and df_mod['T_2M'][j] < 20.0: 
            count_7 = count_7 + 1
        elif df_mod[key][j] >=  20.0 and df_mod['T_2M'][j] < 25.0: 
            count_8 = count_8 + 1
        elif df_mod[key][j] >=  25.0 and df_mod['T_2M'][j] < 30.0: 
            count_9 = count_9 + 1
        else:  
            count_10 = count_10 + 1        
        
    list_num = []
    list_num.extend([count_1, count_2, count_3, count_4, count_5,
                     count_6, count_7, count_8, count_9, count_10])

    return list_num


# end Subroutine get_pdf
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine: DAV_metric
#------------------------------------------------------------------------------
#
# The subroutine needs for DAV calculations
# 
# Input parameters : pr1 - high resolution parameter
#                    pr2 -  low resolution parameter
#                    pr3 - obse  rvations 
#
# Output parameters: DAV - the DAV metric 
#
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def DAV_metric(pr1, pr2, pr3):
    s_hr = 0 
    s_lr = 0

    for j in range(len(pr1)):
        s_hr = s_hr + min(pr1[j], pr3[j])
        
        s_lr = s_lr + min(pr2[j], pr3[j])
    
    
    DAV = (s_hr - s_lr) / s_lr
    return DAV

# end Subroutine DAV_metric
#------------------------------------------------------------------------------





#------------------------------------------------------------------------------
# Subroutine: DAV_analysis
#------------------------------------------------------------------------------
#
# The subroutine needs for DAV calculations
# 
# Input parameters : mf_com          - the main path to folder
#                    sf_data_ref_dav - subfolder for reference data
#                    sf_data_ds_dav  - subfolder for model data
#                    par_list        - the list with parameters
#                    ds_name         - the name of model dataset


# Output parameters: DAV_list - the DAV list for parameters from par_list 
#
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------


def DAV_analysis(mf_com, sf_data_ref_dav, 
                         sf_data_ds_dav ,
                         sf_data_hyras  ,
                         par_list, refer, ds_name):
    
    # The lists for filenames
    dav_name_obs = []
    dav_name_mod = []
    dav_name_hyr = []
    
    for i in range(len(par_list)):
        # FileNames for data
        d_obs  = 'LU_'    + refer    + '_' + par_list[i] + '_mean_obs.csv'
        d_mod  = 'LU_'    + ds_name + '_' + par_list[i] + '_fldmean_mod.csv'
        d_hyr  = 'hyras_' + par_list[i] + '_mean.csv' 
    
        dav_name_obs.append(d_obs)
        dav_name_mod.append(d_mod)
        dav_name_hyr.append(d_hyr)


    # The lists for data path
    iPath_dav_obs = []
    iPath_dav_mod = []
    iPath_dav_hyr = []
    
    for i in range(len(par_list)):
        # Paths for data
        path_d_obs = mf_com + sf_data_ref_dav + dav_name_obs[i]
        path_d_mod = mf_com + sf_data_ds_dav  + dav_name_mod[i]
        path_d_hyr = mf_com + sf_data_hyras   + dav_name_hyr[i]
    
        iPath_dav_obs.append(path_d_obs)
        iPath_dav_mod.append(path_d_mod)
        iPath_dav_hyr.append(path_d_hyr)


    df_list_obs = []    
    df_list_mod = []
    df_list_hyr = []
    
    for i in range(len(par_list)):
        df_dav_obs = get_dav(iPath_dav_obs[i], par_list[i])
        df_dav_mod = get_dav(iPath_dav_mod[i], par_list[i])
        df_dav_hyr = get_dav(iPath_dav_hyr[i], par_list[i])
    
        df_list_obs.append(df_dav_obs)    
        df_list_mod.append(df_dav_mod) 
        df_list_hyr.append(df_dav_hyr)
        
    
    df_obs = pd.concat(df_list_obs, axis = 1)
    df_mod = pd.concat(df_list_mod, axis = 1)
    df_hyr = pd.concat(df_list_hyr, axis = 1)
    
    df_obs = df_obs.resample('D').mean()
    df_mod = df_mod.resample('D').mean()
    df_hyr = df_hyr.resample('D').mean()
    
    
    for j in range(len(df_obs)):
        if df_obs['TOT_PREC'][j] < 0.09:
            df_obs['TOT_PREC'][j] = 0.0
    
    for j in range(len(df_mod)):
        if df_mod['TOT_PREC'][j] < 0.09:
            df_mod['TOT_PREC'][j] = 0.0        
        
    for j in range(len(df_hyr)):
        if df_hyr['TOT_PREC'][j] < 0.09:
            df_hyr['TOT_PREC'][j] = 0.0



    # Create PDF for temperature
    t2m_mean_obs = get_pdf(df_obs, par_list[0])
    t2m_mean_mod = get_pdf(df_mod, par_list[0])
    t2m_mean_hyr = get_pdf(df_hyr, par_list[0])
    
    # T2m_max   
    t2m_max_obs  = get_pdf(df_obs, par_list[1])
    t2m_max_mod  = get_pdf(df_mod, par_list[1])
    t2m_max_hyr  = get_pdf(df_hyr, par_list[1])
    
    #T2m_min
    t2m_min_obs  = get_pdf(df_obs, par_list[2])
    t2m_min_mod  = get_pdf(df_mod, par_list[2])
    t2m_min_hyr  = get_pdf(df_hyr, par_list[2])
    
    # TOT_PREC
    tot_prec_obs = get_pdf(df_obs, par_list[3])
    tot_prec_mod = get_pdf(df_mod, par_list[3])
    tot_prec_hyr = get_pdf(df_hyr, par_list[3])       
    
    # Calculate DAV metric
    DAV_t2m_mean = DAV_metric(t2m_mean_mod, t2m_mean_obs, t2m_mean_hyr)
    DAV_t2m_max  = DAV_metric(t2m_max_mod , t2m_max_obs , t2m_max_hyr )
    DAV_t2m_min  = DAV_metric(t2m_min_mod , t2m_min_obs , t2m_min_hyr )
    DAV_prec_tot = DAV_metric(tot_prec_mod, tot_prec_obs, tot_prec_hyr)
    
    print('DAV_T2M_MEAN ', "{:.3f}".format(DAV_t2m_mean), '\n')
    print('DAV_T2M_MAX ' , "{:.3f}".format(DAV_t2m_max ), '\n')
    print('DAV_T2M_MIN ' , "{:.3f}".format(DAV_t2m_min ), '\n')
    print('DAV_TOT_PREC ', "{:.3f}".format(DAV_prec_tot), '\n')


    DAV_list = []
    DAV_list.extend([DAV_t2m_mean, DAV_t2m_max , 
                     DAV_t2m_min , DAV_prec_tot])
    
    
    return DAV_list

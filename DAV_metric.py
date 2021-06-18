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

def get_pdf(data_array):
    
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
        if df_mod[j] < -10.0:
            count_1 = count_1 + 1
        elif df_mod[j] >= -10.0 and df_mod[j] < -5.0:
            count_2 = count_2 + 1
        elif df_mod[j] >= -5.0  and df_mod[j] < -0.0: 
            count_3 = count_3 + 1
        elif df_mod[j] >=  0.0  and df_mod[j] <  5.0: 
            count_4 = count_4 + 1
        elif df_mod[j] >=  5.0  and df_mod[j] < 10.0: 
            count_5 = count_5 + 1
        elif df_mod[j] >=  10.0 and df_mod[j] < 15.0: 
            count_6 = count_6 + 1
        elif df_mod[j] >=  15.0 and df_mod[j] < 20.0: 
            count_7 = count_7 + 1
        elif df_mod[j] >=  20.0 and df_mod[j] < 25.0: 
            count_8 = count_8 + 1
        elif df_mod[j] >=  25.0 and df_mod[j] < 30.0: 
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
 

def DAV_analysis(mf_com, sf_obs_data, 
                         sf_lr_data ,
                         sf_hr_data ,
                         par_list, refer, ds_name):



        
    # FileNames for data
    d_obs = refer + '_'   + par_list + '_mean.csv'
    d_lr  = 'COSMO_ORIG_' + par_list + '_mean_daily.csv'
    d_hr  = ds_name + '_' + par_list + '_mean_daily.csv'    
    
    # Paths for data
    path_obs = mf_com + sf_obs_data + d_obs
    path_lr  = mf_com + sf_lr_data  + d_lr
    path_hr  = mf_com + sf_hr_data  + d_hr

 
          

    df_dav_obs = get_dav(path_obs, 'OBS')
    df_dav_lr  = get_dav(path_lr, 'LR')
    df_dav_hr  = get_dav(path_hr, 'HR')
         
    df_data = pd.concat([df_dav_obs, df_dav_lr, df_dav_hr], axis = 1)        
      
    
    # Create PDF for temperature
    obs = get_pdf(df_data['OBS'])
    lr  = get_pdf(df_data['LR'] )
    hr  = get_pdf(df_data['HR'] )
             
        
    # Calculate DAV metric
    dav = DAV_metric(hr, lr, obs)
    
    return dav
        #print('DAV ', "{:.3f}".format(dav), '\n')






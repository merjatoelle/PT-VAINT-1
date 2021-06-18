# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:22:19 2021

@author: churiulin
"""

import math
import numpy as np
import pandas as pd

#------------------------------------------------------------------------------
# Subroutine: get_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual COSMO data
#
# 
# Input parameters : path     - path for data
#                    par_name - name of columns   
#
#
# Output parameters: df_euronet - the data frame with information about EURONET data
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 24.03.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------


def get_data(path, par_name):
    df = pd.read_csv(path, skiprows = 0, sep=' ', skipinitialspace = True, 
                     header = None, parse_dates = {'Date':[0,1]}, index_col = 0,
                     na_values = ['9990','********','***','******'])
    df.columns = [par_name]  
 
    return df


# end Subroutine get_data
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine: KGE_RMSD_analysis
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual COSMO data
#
# 
# Input parameters : mf_com          - the main path to folder
#                    sf_data_ref_dav - subfolder for reference data
#                    sf_data_ds_dav  - subfolder for model data
#                    par_list        - the list with parameters
#                    ds_name         - the name of model dataset  
#
#
# Output parameters: lat - latitude
#                    lon - longitude
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 24.03.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def KGE_RMSD_analysis(mf_com, sf_data_ref, sf_data_ds, par_list, refer, ds_name):   
                 
    # FileNames for data
    m_obs  = refer   + '_' + par_list + '_mean.csv'
    s_obs  = refer   + '_' + par_list + '_std.csv'
    m_mod  = ds_name + '_' + par_list + '_mean_daily.csv'
    s_mod  = ds_name + '_' + par_list + '_std_daily.csv'    
    c_name = 'Corr_' + refer + '_' + ds_name + '_' + par_list + '.csv'
                

                 
    path_m_obs = mf_com + sf_data_ref + m_obs
    path_s_obs = mf_com + sf_data_ref + s_obs
    path_m_mod = mf_com + sf_data_ds  + m_mod
    path_s_mod = mf_com + sf_data_ds  + s_mod
    path_c     = mf_com + sf_data_ds  + c_name
        

       
               

    df_mean_obs = get_data(path_m_obs, 'M_obs' )
    df_std_obs  = get_data(path_s_obs , 'S_obs' )
    df_mean_mod = get_data(path_m_mod, 'M_mod' )
    df_std_mod  = get_data(path_s_mod , 'S_mod' )
    df_corr     = get_data(path_c    , 'P'     )
               
    
    # Observation data    
    std_obs  = np.mean(df_std_obs)[0]
    mean_obs = np.mean(df_mean_obs)[0]      
    
    # Model data
    std_mod  = np.mean(df_std_mod)[0] 
    mean_mod = np.mean(df_mean_mod)[0]  
        
    # Correlation
    corr = np.mean(df_corr)[0]

        
    kge = 1.0 - math.sqrt((corr - 1.0 )**2.0 + (std_mod  / std_obs  - 1.0 )**2.0 +               
                                                   (mean_mod / mean_obs - 1.0 )**2.0 )     
         
    rmsd = np.sqrt(std_obs**2.0 + std_mod**2.0 - 2.0 * std_obs * std_mod * corr)  
              
    

    return kge, rmsd, corr
    

      





























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
                     na_values = ['9990','********','***','******'])
    df = df.drop(['#', 'value', 'Unnamed: 5'], axis = 1 )
    df.columns = ['lon', 'lat', par_name]  
    
    df = df.drop(['lon', 'lat'], axis = 1 )
    
    return df


# end Subroutine get_data
#------------------------------------------------------------------------------


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


def get_grid(path, par_name):
    df = pd.read_csv(path, skiprows = 0, sep=' ', skipinitialspace = True, 
                     na_values = ['9990','********','***','******'])
    df = df.drop(['#', 'value', 'Unnamed: 5'], axis = 1 )
    df.columns = ['lon', 'lat', par_name]  
    
    df = df.drop([par_name], axis = 1 )
    
    lon = df['lon']
    lat = df['lat']
    
    return lon, lat

# end Subroutine get_grid
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
    

    # The lists for filenames
    mean_name_obs = []
    mean_name_mod = []
    std_name_obs  = []
    std_name_mod  = []
    cor_name      = []

    for i in range(len(par_list)):
        # FileNames for data
        m_obs  = 'LU_'           + refer   + '_' + par_list[i] + '_mean_obs.csv'
        s_obs  = 'LU_'           + refer   + '_' + par_list[i] + '_std_obs.csv'
        m_mod  = 'LU_'           + ds_name + '_' + par_list[i] + '_mean_mod.csv'
        s_mod  = 'LU_'           + ds_name + '_' + par_list[i] + '_std_mod.csv'    
        c_name = 'Corr_' + refer + '_LU_' + ds_name + '_' + par_list[i] + '.csv'
        
        mean_name_obs.append(m_obs)
        std_name_obs.append(s_obs)    
        mean_name_mod.append(m_mod)
        std_name_mod.append(s_mod)
        cor_name.append(c_name)


    # The lists for data path
    iPath_mean_obs = []
    iPath_mean_mod = []
    iPath_std_obs  = []
    iPath_std_mod  = []
    iPath_corr     = []

    for i in range(len(par_list)):
        # Paths for data
        path_m_obs = mf_com + sf_data_ref + mean_name_obs[i]
        path_s_obs = mf_com + sf_data_ref + std_name_obs[i]
        path_m_mod = mf_com + sf_data_ds  + mean_name_mod[i]
        path_s_mod = mf_com + sf_data_ds  + std_name_mod[i]
        path_c     = mf_com + sf_data_ds  + cor_name[i]
        
        iPath_mean_obs.append(path_m_obs)
        iPath_std_obs.append(path_s_obs)
        iPath_mean_mod.append(path_m_mod)
        iPath_std_mod.append(path_s_mod)
        iPath_corr.append(path_c)
        

    # create a list for dataframes
    df_data_list = []    
    
    for i in range(len(par_list)):
        df_mean_obs = get_data(iPath_mean_obs[i], 'M_obs' )
        df_std_obs  = get_data(iPath_std_obs[i] , 'S_obs' )
        df_mean_mod = get_data(iPath_mean_mod[i], 'M_mod' )
        df_std_mod  = get_data(iPath_std_mod[i] , 'S_mod' )
        df_corr     = get_data(iPath_corr[i]    , 'P'     )
        
        lon,lat     = get_grid(iPath_mean_obs[i], 'M_obs' )
        
        
        df_data = pd.concat([lon, lat, df_mean_obs, df_std_obs, df_mean_mod, df_std_mod,
                             df_corr ], axis = 1)
    
        df_data_list.append(df_data)
    
    
    # Create a new list for kge and rmsd timeseries    
    kge_list  = []
    rmsd_list = []

    for i in range(len(df_data_list)):
        # Create two zero timeseries
        kge = pd.Series(np.nan , index = df_data_list[i].index, name = 'KGE' )
        RMSD = pd.Series(np.nan, index = df_data_list[i].index, name = 'RMSD')
        kge_list.append(kge)
        rmsd_list.append(RMSD)
 
    
    # 
    #rmsd_refer_list = [] 
    corr_field_list = [] 
    for j in range(len(df_data_list)):
        #ref_std = np.mean(df_data_list[j]['S_obs'])
        #ref_rmsd = math.sqrt(ref_std**2.0 - 2.0 * ref_std)
        #rmsd_refer_list.append(ref_rmsd)
        #print('RMSD ' + ds_name + '_' + par_list[j] + ' - ', rmsd_refer_list[j])

    
        ref_corr = np.mean(df_data_list[j]['P'])
        corr_field_list.append(ref_corr)   
        
        
        
        
        #print('CORR ' + ds_name + '_' + par_list[j] + ' - ', corr_field_list[j], '\n')
        print('CORR ' + ds_name + '_' + par_list[j] + ' - ',  
              "{:.3f}".format(corr_field_list[j]), '\n')
   
  
 
    for j in range(len(df_data_list)):
        print (par_list[j], '\n')
        for row in range(len(df_data_list[j])):
            
            kge_list[j][row] = 1.0 - math.sqrt((df_data_list[j]['P'][row] - 1.0 )**2.0 + 
                                               (df_data_list[j]['S_mod'][row] / df_data_list[j]['S_obs'][row] - 1.0 )**2.0 +
                                               (df_data_list[j]['M_mod'][row] / df_data_list[j]['M_obs'][row] - 1.0 )**2.0 ) 
        
   
            try:
                rmsd_list[j][row] = math.sqrt( (df_data_list[j]['S_obs'][row])**2.0 + 
                                               (df_data_list[j]['S_mod'][row])**2.0 -
                                                2.0 * df_data_list[j]['S_obs'][row] * 
                                                      df_data_list[j]['S_mod'][row] * 
                                                      df_data_list[j]['P'][row])  
            except ValueError as error:
                    print ( 'Line: ', row, 'Parameter ', par_list[j], 'sqrt(0) ', error , '\n')
                    rmsd_list[j][row] = 0.0      

    
    kge_field_list  = []
    rmsd_field_list = []
    
    for k in range(len(kge_list)):
        kge_field = np.mean(kge_list[k])
        rmsd_field = np.mean(rmsd_list[k])
        kge_field_list.append(kge_field)
        rmsd_field_list.append(rmsd_field)
    
    
        print ('kge '  + ds_name + '_' + par_list[k] + ' - ', "{:.3f}".format(kge_field_list[k] ), '\n')
        print ('rmsd ' + ds_name + '_' + par_list[k] + ' - ', "{:.3f}".format(rmsd_field_list[k]), '\n')

    
    return kge_list, rmsd_list, kge_field_list, rmsd_field_list, corr_field_list
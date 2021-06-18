# -*- coding: utf-8 -*-
"""
The KGE_RMSD metric is the program for calculation the root-mean-square error (RMSE)
and the Kling-Gupta-Efficiency (KGE) index (Gupta et al., 2009) 
Gupta, H.V. Kling, H. Yilmaz, K.K. Martinez, G.F.: Decomposition of the mean 
squared error and NSE performance criteria: Implications for improving 
hydrological modelling. J. Hydrol. 2009, 377, 80–91. 
https://doi.org/10.1016/j.jhydrol.2009.08.003   

The DAV_metric is the program for calculation the distribution added value (DAV)
index based on work (Soares and Cardoso, 2017).
Soares, P.M.M. Cardoso, R.M.: A simple method to assess the added value using 
high-resolution climate distributions: Application to the EURO-CORDEX daily 
precipitation. Int. J. Climatol. 2017, 38, 1484–1498.
https://doi.org/10.1002/joc.5261                
                                      
The progam contains several subroutines for:
    
    KGE and RMSD analysis:
        get_data          ---> The subroutine needs for getting actual COSMO data
        get_grid          ---> The subroutine needs for getting probability density function
        KGE_RMSD_analysis ---> The subroutine needs for statistical analysis of the datasets        
    
    DAV analysis:
        get_dav           ---> The subroutine needs for getting data for DAV analisis 
        get_pdg           ---> The subroutine needs for getting probability density function
        DAV_metric        ---> The subroutine needs for DAV calculations
        DAV_analysis      ---> The subroutine needs for DAV calculations

                                                
Autors of project: Evgenii Churiulin, Merja Tölle, Center for Enviromental 
                                                   System Research (CESR) 
                                                   
Current Code Owner: CESR, Evgenii Churiulin
phone:  +49  561 804-6142
fax:    +49  561 804-6116
email:  evgenychur@uni-kassel.de
History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    2021-06-18 Evgenii Churiulin, Center for Enviromental System Research (CESR)
           Initial release
                 
"""

import math
import numpy as np
import pandas as pd


#------------------------------------------------------------------------------
# Subroutine: get_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual information from dataset
# 
# Input parameters : path     - path for data
#                    par_name - name of columns   
#
# Output parameters: df - the data frame with information about interesting 
#                         parameter
#------------------------------------------------------------------------------
def get_data(path, par_name):
    df = pd.read_csv(path, skiprows = 0, sep=' ', skipinitialspace = True, 
                     na_values = ['-999','-1','***','******'])
    df = df.drop(['#', 'value', 'Unnamed: 5'], axis = 1 )
    df.columns = ['lon', 'lat', par_name]  
    
    df = df.drop(['lon', 'lat'], axis = 1 )
    
    return df


""" # Old version
def get_data(path, par_name):
    df = pd.read_csv(path, skiprows = 0, sep=' ', skipinitialspace = True, 
                     header = None, parse_dates = {'Date':[0,1]}, index_col = 0,
                     na_values = ['9990','********','***','******'])
    df.columns = [par_name]  
    return df
"""
# end Subroutine get_data
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Subroutine: get_grid
#------------------------------------------------------------------------------
# The subroutine needs for getting actual information about longitude and latitude
# for current grid
# 
# Input parameters : path     - path for data
#                    par_name - name of columns    
#
# Output parameters: lat - latitude
#                    lon - longitude
#------------------------------------------------------------------------------
def get_grid(path, par_name):
    df = pd.read_csv(path, skiprows = 0, sep=' ', skipinitialspace = True, 
                     na_values = ['-999','-1','***','******'])
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
# The subroutine needs for statistical analysis of the datasets
#
# Input parameters : mf_com          - the main path to folder
#                    sf_data_ref_dav - subfolder for reference data
#                    sf_data_ds_dav  - subfolder for model data
#                    par_list        - the list with parameters
#                    refer           - the name of reference data set 
#                    ds_name         - the name of model dataset  
#
# Output parameters: statistical parameters in a pront version
#------------------------------------------------------------------------------

def KGE_RMSD_analysis(path_main, fn_region, par_list, refer, ds_name):
    
    # FileNames for data
    m_obs  = refer   + '_' + par_list + '_mean_' + fn_region + '_domain.csv'
    s_obs  = refer   + '_' + par_list + '_std_'  + fn_region + '_domain.csv'
    m_mod  = ds_name + '_' + par_list + '_mean_' + fn_region + '_domain.csv'
    s_mod  = ds_name + '_' + par_list + '_std_'  + fn_region + '_domain.csv'   
    c_name = 'Corr_' + refer + '_' + ds_name + '_' + par_list + '_' + fn_region + '_domain.csv'
    
    # Path for data
    path_m_obs = path_main + m_obs
    path_s_obs = path_main + s_obs
    path_m_mod = path_main  + m_mod
    path_s_mod = path_main  + s_mod
    path_c     = path_main  + c_name
        
        
    # Get data    
    df_mean_obs = get_data(path_m_obs, 'M_obs' )
    df_std_obs  = get_data(path_s_obs, 'S_obs' )
    df_mean_mod = get_data(path_m_mod, 'M_mod' )
    df_std_mod  = get_data(path_s_mod, 'S_mod' )
    df_corr     = get_data(path_c    , 'P'     )
                           
    # Get coordinates
    lon,lat     = get_grid(path_m_obs, 'M_obs' )   
     
    # Combine in one dataframe
    df_data = pd.concat([lon, lat, df_mean_obs, df_std_obs, df_mean_mod, 
                                    df_std_mod, df_corr  ], axis = 1)
    
    # Delete nan values
    df_data = df_data.dropna()
    # Reset index
    df_data = df_data.reset_index()
    # Delete previous index
    df_data = df_data.drop(['index'], axis = 1 )

    

    # Create two zero timeseries
    kge  = pd.Series(np.nan, index = df_data.index, name = 'KGE' )
    rmsd = pd.Series(np.nan, index = df_data.index, name = 'RMSD')
        
    # Get correlation values
    ref_corr = np.mean(df_data['P'])
    print('CORR ' + ds_name + '_' + par_list + ' - ',  
              "{:.3f}".format(ref_corr), '\n')    

   
    # Get KGE and RMSD
 
    for row in range(len(df_data)):
            
        kge[row] = 1.0 - math.sqrt((df_data['P'][row] - 1.0 )**2.0 + 
                                   (df_data['S_mod'][row] / df_data['S_obs'][row] - 1.0 )**2.0 +
                                   (df_data['M_mod'][row] / df_data['M_obs'][row] - 1.0 )**2.0 ) 

        #print (row, '-', len(kge))        
        if row == (len(kge) - 1):
            print ('hel')
            if kge[row] < -1.5:
                kge[row] = kge[row - 1]

        else:
            if kge[row] < -1.5:
                kge[row] = (kge[row-1] + kge[row+1]) / 2.0

        
        try:
            rmsd[row] = math.sqrt((df_data['S_obs'][row])**2.0 + 
                                  (df_data['S_mod'][row])**2.0 -
                                  2.0 * df_data['S_obs'][row] * 
                                        df_data['S_mod'][row] * 
                                        df_data['P'][row])  
            
        except ValueError as error:
            #print ( 'Line: ', row, 'Parameter ', par, 'sqrt(0) ', error , '\n')
            rmsd[row] = -1.0 * math.sqrt( abs((df_data['S_obs'][row])**2.0 + 
                                              (df_data['S_mod'][row])**2.0 -
                                              2.0 * df_data['S_obs'][row] * 
                                                    df_data['S_mod'][row] * 
                                                    df_data['P'][row]))        
        
   
    ref_kge  = np.mean(kge)
    ref_rmsd = np.mean(rmsd)
    
    return ref_kge, ref_rmsd, ref_corr  



    """ Old version
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
    """
#------------------------------------------------------------------------------






#------------------------------------------------------------------------------
# Subroutine: get_dav
#------------------------------------------------------------------------------
# The subroutine needs for getting data for DAV analisis
# 
# Input parameters : iPath   - absolute path for data
#                    ts_name - the name of parameter for analysis   
#
# Output parameters: ts      - timeseries with intersting parameter 
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
# The subroutine needs for getting probability density function
# 
# Input parameters : data_array - array with data
#
# Output parameters: list_num   - probability density function  
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
# The subroutine needs for DAV calculations
# 
# Input parameters : pr1 - high resolution parameter
#                    pr2 -  low resolution parameter
#                    pr3 - obse  rvations 
#
# Output parameters: DAV - the DAV metric 
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
# The subroutine needs for DAV calculations
# 
# Input parameters : mf_com      - the main path to folder
#                    sf_obs_data - subfolder for reference data
#                    sf_lr_data  - subfolder for model data
#                    par_list    - the list with parameters
#                    refer       - the name of dataset
#                    ds_name     - the name of model dataset
#
# Output parameters: DAV_list - the DAV list for parameters from par_list 
#------------------------------------------------------------------------------
def DAV_analysis(path_main, fn_region,  par_list, refer, ds_name):      
    # FileNames for data
    d_obs = refer + '_'   + par_list + '_mean_dav_' + fn_region + '_domain.csv'
    d_lr  = 'COSMO_ORIG_' + par_list + '_mean_dav_' + fn_region + '_domain.csv'
    d_hr  = ds_name + '_' + par_list + '_mean_dav_' + fn_region + '_domain.csv'      
    
    # Paths for data
    path_obs = path_main + d_obs
    path_lr  = path_main + d_lr
    path_hr  = path_main + d_hr       
    
    # Get data
    df_dav_obs = get_dav(path_obs, 'OBS')
    df_dav_lr  = get_dav(path_lr, 'LR')
    df_dav_hr  = get_dav(path_hr, 'HR')
    # Combine data in one dataset     
    df_data = pd.concat([df_dav_obs, df_dav_lr, df_dav_hr], axis = 1)               
    # Create PDF for temperature
    obs = get_pdf(df_data['OBS'])
    lr  = get_pdf(df_data['LR'] )
    hr  = get_pdf(df_data['HR'] )
    # Calculate DAV metric
    dav = DAV_metric(hr, lr, obs)    
    return dav













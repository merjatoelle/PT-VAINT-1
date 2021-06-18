# -*- coding: utf-8 -*-
"""
The cosmo_data is the program for work with COSMO data.

The progam contains several additional subroutines:
    get_data          ---> The subroutine needs for getting actual COSMO data
    cosmo_data        ---> The subroutine needs for getting actual COSMO data 
    get_timeseries    ---> The subroutine needs for getting actual timeseries 
                           from COSMO dataframes 
    cosmo_montly_data ---> Get mean values by month (climatic mean - annual cycles) 
    cosmo_daily_data  ---> Get mean daily values by days for each June
    cosmo_hourly_data ---> Get mean hourly data (duirnal cycle)
    stat_cosmo        ---> The subroutine needs for getting actual statistical
                           parameters acording to COSMO data 
  
Autors of project: Evgenii Churiulin, Merja Tölle, Center for Enviromental System
                                                   Research (CESR) 

                                                   
Current Code Owner: CESR, Evgenii Churiulin
phone:  +49  561 804-6142
fax:    +49  561 804-6116
email:  evgenychur@uni-kassel.de


History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    2021-04.15 Evgenii Churiulin, Center for Enviromental System Research (CESR)
           Initial release
                 
"""

# Import standart liblaries
import gc
import numpy as np
import pandas as pd

# Improt methods for statistical analysis
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


#------------------------------------------------------------------------------
# Subroutine: get_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual COSMO data
# 
# Input parameters : data_path         - path for COSMO data
#                    parameter_name    - name of parameter   
#
# Output parameters: ts - the timeseries with data
#------------------------------------------------------------------------------

def get_data(data_path, parameter_name):
    
    df = pd.read_csv(data_path, skiprows = 0, sep=' ', parse_dates = {'Date':[0,1]},
                     header = None, index_col = 0, skipinitialspace = True, 
                     na_values = ['9990','********','***','******'])
    df.columns = [parameter_name]
    ts = df[parameter_name]
    #print(parameter_name)
    #ts = ts[ts.index.duplicated()]
    ts = ts[~ts.index.duplicated()]
    return ts
    gc.collect() 
# end def get data
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine: cosmo_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual COSMO data
# 
# Input parameters : main_path - general path for research project
#                    sf_path   - name of subfolder for COSMO data  
#                    fn_prefix - name of COSMO run (original or experiment)
#                    clm_name  - names of COSMO parameters   
#
# Output parameters: df_cosmo - the data frame with information about COSMO data
#------------------------------------------------------------------------------
def cosmo_data(main_path, sf_path, fn_prefix, clm_name):
    # mian path
    mf_com = main_path
    # subfolder
    sf_cosmo = sf_path
    # the main prefix
    fn_cosmo = fn_prefix
    # Name of columns and files
    columns_name = clm_name   
    #--------------------------------------------------------------------------
    # Define actual filename for COSMO data
    #--------------------------------------------------------------------------
    fn_list = []
    for fn in range(len(columns_name)):
        name_file = columns_name[fn] + fn_cosmo
        fn_list.append(name_file)
    #--------------------------------------------------------------------------
    # Define paths for COSMO data 
    #--------------------------------------------------------------------------   
    iPath = [] 
    for i in range(len(columns_name)):
        path = mf_com + sf_cosmo + fn_list[i]
        iPath.append(path)    
    #--------------------------------------------------------------------------   
    # Get data
    #--------------------------------------------------------------------------     
    df_list = []
    for j in range(len(iPath)):
        data =  get_data(iPath[j], columns_name[j])     
        df_list.append(data)            
    df_cosmo = pd.concat(df_list, axis = 1)
    return df_cosmo  
# end def cosmo_data
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine: get_timeseries
#------------------------------------------------------------------------------
# The subroutine needs for getting actual timeseries from COSMO dataframes
# 
# Input parameters : clm_name - name of COSMO parameters 
#                    data_ts  - columns name from list 
#                    period   - time period 
#                    ts       - step for resampling
#
# Output parameters: parc_list - the list of COSMO parameters 
#------------------------------------------------------------------------------
def get_timeseries(clm_name, data_ts, period, ts):   
    t0melt = 273.15

    parc_list = []
    for i in range(len(clm_name)):
        if ts == None:
            # Date without resemple
            if clm_name[i] in ('ALHFL_BS','ALHFL_PL','ALHFL_S', 'ASHFL_S'):
                par_parc01 = data_ts[clm_name[i]][period] * -1.0
            elif clm_name[i] in ('AEVAP_S'):
                par_parc01 = data_ts[clm_name[i]][period] * -1.0               
            elif clm_name[i] in ('T_2M','T_S', 'TMAX_2M', 'TMIN_2M'):
                par_parc01 = data_ts[clm_name[i]][period] - t0melt
            elif clm_name[i] == 'PS':
                #par_parc01 = (data_ts[clm_name[i]][period] / 100.0).interpolate()                        # [hPa]
                par_parc01 = data_ts[clm_name[i]][period] / 100.0
            elif clm_name[i] in ('ZTRALEAV', 'ZTRANG', 'ZTRANGS', 'ZVERBO'):
                par_parc01 = data_ts[clm_name[i]][period] * -1.0 * 10e4
            elif clm_name[i] in ('RSTOM'):
                for j in range(len(data_ts[clm_name[i]])):
                    if data_ts[clm_name[i]][j] > 20000.0:
                        data_ts[clm_name[i]][j] = 20000.0                                           
                par_parc01 = data_ts[clm_name[i]][period]               
            else:
                par_parc01 = data_ts[clm_name[i]][period]                       
        else:
            # Date where we have to use resample step
            if clm_name[i] in ('ALHFL_BS','ALHFL_PL','ALHFL_S', 'ASHFL_S'):
                par_parc01 = data_ts[clm_name[i]][period].resample(ts).mean()  * -1.0
            elif clm_name[i] in ('AEVAP_S'):
                par_parc01 = data_ts[clm_name[i]][period].resample(ts).sum()  * -1.0
            elif clm_name[i] in ('T_2M', 'T_S', 'TMAX_2M', 'TMIN_2M'):
                par_parc01 = data_ts[clm_name[i]][period].resample(ts).mean() - t0melt                
            elif clm_name[i] == 'PS':
                #par_parc01 = ((data_ts[clm_name[i]][period].resample(ts).mean()) / 100.0).interpolate()  # [hPa]
                par_parc01 = (data_ts[clm_name[i]][period].resample(ts).mean()) / 100.0  # [hPa]                
            elif clm_name[i] in ('ZTRALEAV', 'ZTRANG', 'ZTRANGS', 'ZVERBO'):
                par_parc01 = data_ts[clm_name[i]][period].resample(ts).mean() * -1.0  * 10e4                  
            elif clm_name[i] in ('RSTOM'):
                for j in range(len(data_ts[clm_name[i]])):
                    if data_ts[clm_name[i]][j] > 20000.0:
                        data_ts[clm_name[i]][j] = 20000.0                                           
                par_parc01 = data_ts[clm_name[i]][period].resample(ts).mean()         
            else:
                par_parc01 = data_ts[clm_name[i]][period].resample(ts).mean()
        
        parc_list.append(par_parc01)
        
    return parc_list
# end def get_timeseries
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutines: cosmo_montly_data, cosmo_daily_data, cosmo_hourly_data
#------------------------------------------------------------------------------
# The subroutines needs for getting timeseries values based on mean cosmo values
# 
#       cosmo_montly_data ---> mean values by month (climatic mean - annual cycles) 
#       cosmo_daily_data  ---> mean daily values by days for one June
#       cosmo_hourly_data ---> mean hourly data (duirnal cycle)  
# 
# Input parameters : clm_name - parameters of COSMO fpr analysis
#                    data     - COSMO data
#                    period   - timeperiod for analysis
#                    ts       - timestep for resampling
#                    t1, t2   - dates for period
#         
# Output parameters: dataframe - dataframe with mean parameters 
#------------------------------------------------------------------------------

def cosmo_montly_data(clm_name, data, period, ts):   
    data_cosmo = get_timeseries(clm_name, data, period, ts)             
    df_parc = pd.concat(data_cosmo, axis = 1)
    df_parc = df_parc.reset_index()
    mon_id  = df_parc['index'].dt.month
    parc_m  = df_parc.groupby(mon_id).mean()
    # Re-indexing
    time_index = pd.date_range('1/1/2019', '12/1/2019', freq='MS').strftime('%B')
    parc_m.index  = time_index    
    return parc_m

def cosmo_daily_data(t_1, t_2, clm_name, data, ts):    
    list_cosmo_years = []
    list_cosmo_param = []    
    for  tr in range(len(t_1)):
        # Get a time period
        period = pd.date_range(t_1[tr], t_2[tr], freq = '1H')            
        parc   = get_timeseries(clm_name, data, period, ts)  
        # Concat data in data frame for each year
        df_year = pd.concat(parc, axis = 1)
        # Add year to general list for all year
        list_cosmo_years.append(df_year)   
    # Concat all year in on dataframe
    df_parc = pd.concat(list_cosmo_years, axis = 1)
    # Reset index
    df_parc = df_parc.reset_index()
    # Get day index in June 
    d_id    = df_parc['index'].dt.day
    for i in range(len((clm_name))):
        # Get data for each parameter
        param = df_parc[clm_name[i]].groupby(d_id).mean()
        param = param.mean(axis = 1)
        param = param.rename(clm_name[i])   
        # Add data to lists     
        list_cosmo_param.append(param)       
    # Get data    
    df_cosmo = pd.concat(list_cosmo_param, axis = 1)   
    return df_cosmo

def cosmo_hourly_data(t_1h, t_2h, clm_name, data):    
    list_cosmo_years = []
    list_cosmo_param  = []    
    for  tr in range(len(t_1h)):
        # Get a time period
        period = pd.date_range(t_1h[tr], t_2h[tr], freq = '1H')            
        ts = None
        parc   = get_timeseries(clm_name, data, period, ts)  
        # Concat data in data frame for each year
        df_year = pd.concat(parc, axis = 1)
        # Add year to general list for all year
        list_cosmo_years.append(df_year)    
    # Concat all year in on dataframe
    df_parc = pd.concat(list_cosmo_years, axis = 1)
    # Reset index
    df_parc = df_parc.reset_index()
    # Get day index in June 
    d_id    = df_parc['index'].dt.hour
    for i in range(len((clm_name))):
        # Get data for each parameter
        param = df_parc[clm_name[i]].groupby(d_id).mean()
        param = param.mean(axis = 1)
        param = param.rename(clm_name[i])    
        # Add data to lists     
        list_cosmo_param.append(param)       
    # Get data    
    df_cosmo = pd.concat(list_cosmo_param, axis = 1)   
    return df_cosmo
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine: stat_cosmo
#------------------------------------------------------------------------------
# The subroutine needs for getting actual statistical parameters acording to 
# COSMO data 
#
# 
# Input parameters : clm_name - name of COSMO parameters 
#                    df_ctr   - dataset with COSMO_CTR data 
#                    df_mod   - dataset with COSMO experiment data 
#
# Output parameters: df_stat_cosmo - the dataframe with statistical parameters
#------------------------------------------------------------------------------
def stat_cosmo(clm_name, df_ctr, df_mod):
    # Create a nan timeseries
    mean_orig = pd.Series(np.nan, index = range(len(clm_name)))
    max_orig  = pd.Series(np.nan, index = range(len(clm_name))) 
    min_orig  = pd.Series(np.nan, index = range(len(clm_name)))
    mean_exp  = pd.Series(np.nan, index = range(len(clm_name)))
    max_exp   = pd.Series(np.nan, index = range(len(clm_name)))
    min_exp   = pd.Series(np.nan, index = range(len(clm_name)))
    std_orig  = pd.Series(np.nan, index = range(len(clm_name)))
    std_exp   = pd.Series(np.nan, index = range(len(clm_name)))
    mae       = pd.Series(np.nan, index = range(len(clm_name)))
    rmse      = pd.Series(np.nan, index = range(len(clm_name)))
    corr      = pd.Series(np.nan, index = range(len(clm_name)))
    
    # Start calculations
    for i in range(len(clm_name)):
        mean_orig[i] = df_ctr[clm_name[i]].mean()
        max_orig[i]  = df_ctr[clm_name[i]].max()
        min_orig[i]  = df_ctr[clm_name[i]].min()
        std_orig[i]  = df_ctr[clm_name[i]].std()
        mean_exp[i]  = df_mod[clm_name[i]].mean()
        max_exp[i]   = df_mod[clm_name[i]].max()
        min_exp[i]   = df_mod[clm_name[i]].min()
        std_exp[i]   = df_mod[clm_name[i]].std()       
        mae[i]       = mean_absolute_error(df_ctr[clm_name[i]], df_mod[clm_name[i]])
        rmse[i]      = mean_squared_error(df_ctr[clm_name[i]], df_mod[clm_name[i]])
        corr[i]      = df_ctr[clm_name[i]].corr(df_mod[clm_name[i]])
    
    # Create data frame
    df_stat_cosmo = pd.DataFrame({'Parameter' : ['AEVAP_S',  'ALHFL_S', 
                                                 'ASHFL_S',  'RSTOM'  ,
                                                 'ZVERBO' ,  'T_2M'   ,
                                                 'T_S'    ,  'TMAX_2M',
                                                 'TMIN_2M','ZTRALEAV'],
                                  'Mean COSMO': mean_orig,
                                  'Mean Model': mean_exp ,
                                  'Max COSMO' : max_orig ,
                                  'Max MODEL' : max_exp  ,
                                  'Min COSMO' : min_orig ,
                                  'Min MODEL' : min_exp  ,
                                  'STD COSMO' : std_orig ,
                                  'STD_MODEL' : std_exp  ,
                                        'MAE' : mae      ,
                                       'RMSE' : rmse     ,
                                       'CORR' : corr     })
    
    df_stat_cosmo.set_index('Parameter', inplace = True)
    
    return df_stat_cosmo


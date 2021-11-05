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
# Input parameters : sf_path   - path for COSMO data  
#                    fn_prefix - name of COSMO run (original or experiment)
#                    clm_name  - names of COSMO parameters   
#
# Output parameters: df_cosmo - the data frame with information about COSMO data
#------------------------------------------------------------------------------
def cosmo_data(sf_path, fn_prefix, clm_name):
    # list with COSMO data --> timeseries
    cosmo_data = []

    for param in clm_name:
        filename = f'{param}{fn_prefix}'
        path     = f'{sf_path}{filename}'
        cosmo_data.append(get_data(path, param))                               # use COSMO function --> get_data
    df_cosmo = pd.concat(cosmo_data, axis = 1)
    return df_cosmo  
# end def cosmo_data
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Subroutine: get_timeseries
#------------------------------------------------------------------------------
# The subroutine needs for getting actual timeseries from COSMO dataframes
# 
# Input parameters : clm_name - name of COSMO parameters 
#                    df_cosmo  - columns name from list 
#                    period   - time period 
#                    ts       - step for resampling
#
# Output parameters: parc_list - the list of COSMO parameters 
#------------------------------------------------------------------------------
def get_timeseries(df_cosmo, clm_name, period, ts):   
    
    t0melt = 273.15

    cosmo_data = []
    
    for param in clm_name:
        # Date where we have to use resample step
        if param in ('ALHFL_BS', 'ALHFL_PL', 'ALHFL_S', 'ASHFL_S'):
            new_data = df_cosmo[param][period].resample(ts).mean() * -1.0        
             
        elif param in ('T_2M', 'T_S', 'TMAX_2M', 'TMIN_2M'):
            new_data = df_cosmo[param][period].resample(ts).mean() - t0melt             
        
        elif param in ('ZTRALEAV', 'ZTRANG', 'ZTRANGS', 'ZVERBO'):
            new_data = df_cosmo[param][period].resample(ts).mean() * -1.0  * 10e4            
        elif param == 'PS':
            #new_data = ((data_ts[param][period].resample(ts).mean()) / 100.0).interpolate()  # [hPa]
            new_data = (df_cosmo[param][period].resample(ts).mean()) / 100.0    # [hPa]          
        
        elif param == 'AEVAP_S':
            new_data = df_cosmo[param][period].resample(ts).sum()  * -1.0  
    
        elif param == 'RSTOM':
            # correct the stomatal resistance data
            for j in range(len(df_cosmo[param])):
                if df_cosmo[param][j] > 20000.0:
                    df_cosmo[param][j] = 20000.0    
            # calculate mean values                                      
            new_data = df_cosmo[param][period].resample(ts).mean()         

        else:
            new_data = df_cosmo[param][period].resample(ts).mean()            
        
        cosmo_data.append(new_data)
    
    df = pd.concat(cosmo_data, axis = 1)
    
    return df                
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

def cosmo_montly_data(data, clm_name, period, ts):   
    df     = get_timeseries(data, clm_name, period, ts)             
    df     = df.reset_index()
    mon_id = df['index'].dt.month                                              # get the current number for each row based on timeindex
    #mon_id  = df_parc['Date'].dt.month
    df_montly = df.groupby(mon_id).mean()
    # Re-indexing
    time_index = pd.date_range('1/1/2019', '12/1/2019', freq='MS').strftime('%B')
    df_montly.index  = time_index    
    return df_montly




def cosmo_daily_data(data, clm_name, periods, ts):    
    # Combine COSMO data for different monthes in one dataframe
    cosmo_years = []   
    for  index in range(len(periods)):
        df = get_timeseries(data, clm_name, periods[index], ts)                  
        cosmo_years.append(df)                                                 # Add year to general list for all year
    df_period = pd.concat(cosmo_years, axis = 1)                               # Concat all year in on dataframe
    
    # Reset index
    df_period = df_period.reset_index()    
    # Get day index in June 
    day_index = df_period['index'].dt.day   
    # Get mean values for simular days
    cosmo_param = []  
    for param in clm_name:
        # Get data for each parameter
        new_data = df_period[param].groupby(day_index).mean()
        new_data = new_data.mean(axis = 1)
        new_data = new_data.rename(param)   
        # Add data to lists     
        cosmo_param.append(new_data)       
    # Get data    
    df_cosmo = pd.concat(cosmo_param, axis = 1)   
    return df_cosmo



def cosmo_hd(data, clm_name, periods, ts):    
    # Combine COSMO data for different monthes in one dataframe   
    cosmo_years = []
    for  index in range(len(periods)):
        df = get_timeseries(data, clm_name, periods[index], ts)  
        cosmo_years.append(df)    
    df_period = pd.concat(cosmo_years, axis = 1)                                 # Concat all year in on dataframe

    # Reset index
    df_period = df_period.reset_index()    
    # Get hour index
    hour_index = df_period['index'].dt.hour
    # Get mean values for simular hours
    cosmo_param  = []     
    for param in clm_name:
        # Get data for each parameter
        new_data = df_period[param].groupby(hour_index).mean()
        new_data = new_data.mean(axis = 1)
        new_data = new_data.rename(param)    
        # Add data to lists     
        cosmo_param.append(new_data)       
    # Get data    
    df_cosmo = pd.concat(cosmo_param, axis = 1)   
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



def data4month(data, clm_name, periods, ts):    
    # Combine COSMO data for different monthes in one dataframe
    cosmo_years = []   
    for  index in range(len(periods)):
        df = get_timeseries(data, clm_name, periods[index], 'D') 
        df = df.resample(ts).mean()                 
        cosmo_years.append(df)                                                 # Add year to general list for all year
    df_period = pd.concat(cosmo_years, axis = 0)  
    df_period = df_period.reset_index()
    return df_period           

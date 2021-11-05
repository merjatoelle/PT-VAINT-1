# -*- coding: utf-8 -*-
"""
The fluxnet_data is the program for work with fluxnet and euronet data.

The progam contains several subroutine:
    data_path    ---> The subroutine needs for getting actual file name 
                      of FLUXNET data                      
    fluxnet_data ---> The subroutine needs for getting actual FLUXNET data
    euronet_data ---> The subroutine needs for getting actual EURONET data   
    montly_data  ---> The subroutines needs for getting timeseries
    daily_data        values based on mean FLUXNET EURONET or GLEAM values
    hourly_data  
  
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
import sys
import numpy as np
import pandas as pd


#------------------------------------------------------------------------------
# Subroutine: fluxnet_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual FLUXNET data
#
# Input parameters : main_path         - general path for research project
#                    sf_path           - name of subfolder for FLUXNET data
#                    mode              - the type of FLUXNET data (FULLSET or ERAI)       
#                    mylist            - the list of meteorological station
#                    st_in     - the actual name of meteorologicl station
#
# Output parameters: df_fluxnet - the data frame with information about fluxnet data
#------------------------------------------------------------------------------
def fluxnet_data(fluxnet_path, st_in):  
    
    #--------------------------------------------------------------------------
    # Define spesial parameters for FLUXNET data
    #--------------------------------------------------------------------------            
    if st_in in ('RuR','RuS'):                                                 # for RuR and Rus 
        date_start  = '2011'                                          
        date_end    = '2014'                                         
        if st_in == 'RuR':                                                     # for RuR 
            st_name4plot = 'Rollesbroich'
        else:                                                                  # for Rus 
            st_name4plot = 'Selhausen Juelich'
    else:                                                                      # for SeH 
        date_start  = '2007'   
        date_end    = '2010'                                         
        st_name4plot = 'Selhausen'              


    date_period = f'{date_start}-{date_end}'   
    print('FLUXNET data period: ', date_period)
     
    #--------------------------------------------------------------------------
    # Section: Load hourly FLUXNET filename. Timestep ---> HH (for all options)
    #--------------------------------------------------------------------------
    folder   = f'FLX_DE-{st_in}/'
    timestep = 'HH'
    fileName = f'FLX_DE-{st_in}_FLUXNET2015_FULLSET_{timestep}_{date_period}_1-4.csv'        
    
    #--------------------------------------------------------------------------
    # Section: Create a path for FLUXNET data. Timestep ---> HH (for all options)
    #--------------------------------------------------------------------------
    iPath_fluxnet = fluxnet_path + folder + fileName
    #--------------------------------------------------------------------------
    # Section: Load data from FLUXNET data
    #--------------------------------------------------------------------------
    def correction(data_in, change_on):
        try:
            date_out  = data_in    
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            date_out = change_on         
        return date_out
       
    df_fluxnet = pd.read_csv(iPath_fluxnet, skiprows = 0, sep=',', dayfirst = True,
                             parse_dates = True, index_col = [0], skipinitialspace = True, 
                             na_values= ['-9999','********'])    

    df_fluxnet = df_fluxnet.drop(['TIMESTAMP_END'], axis=1)
        
    # Create a nan timeseries
    s_zero = pd.Series(np.nan, index = df_fluxnet.index)
  
    # T2m -  air temperature
    t2m = correction(df_fluxnet['TA_F_MDS'], df_fluxnet['TA_F'])
    # TS - soil temperature
    ts  = correction(df_fluxnet['TS_F_MDS_1'], s_zero)    
    # LE - latent heat flux
    le = correction(df_fluxnet['LE_F_MDS'], s_zero)
    # LE_CORR
    le_corr = correction(df_fluxnet['LE_CORR'], s_zero)
    # RE - relative humidity 
    #rh = correction(df_fluxnet['RH'], s_zero)
    # VPD - vapor pressure deficit
    vpd = correction(df_fluxnet['VPD_F'], df_fluxnet['VPD_F'])
    # PA - atmospheric pressure [kPa]     
    pa = correction(df_fluxnet['PA'], df_fluxnet['PA_F']) 
    # SH - sensible heat
    sh = correction(df_fluxnet['H_F_MDS'], s_zero)
    # SH_CORE
    sh_corr = correction(df_fluxnet['H_CORR'], s_zero)
                 
    #----------------------------------------------------------------------
    # Create a dataframe with zero values which is equal --->  -9999   
    #----------------------------------------------------------------------
    df_zero = pd.DataFrame(data = np.full((len(t2m), 2), -9999))
    
    # Get two data series for new series for specific humidity and vapor pressure
    vap_pres = pd.Series(df_zero[0].values, index = t2m.index, dtype = 'float')   
    qv_s     = pd.Series(df_zero[1].values, index = t2m.index, dtype = 'float') 
    
    # Calculete values
    for rfn in range(len(t2m)):
        vap_pres[rfn] = 1000.0 * 461.5 * (t2m[rfn] + 273.15)
        qv_s[rfn]     = 0.622 * vap_pres[rfn] / (pa[rfn] - (1 - 0.622) * vap_pres[rfn])
        
    #----------------------------------------------------------------------
    # Section: Create dataframe and resample it to hourly timestep   
    #----------------------------------------------------------------------       
    
    df_FLUXNET = pd.concat([t2m, ts, le, le_corr, #rh, 
                            vpd, pa, vap_pres, qv_s ,
                            sh , sh_corr],  axis = 1)
            
    df_FLUXNET.columns = ['T2m', 'Ts', 'LE', 'LE_corr', #'RH',
                          'VPD','Pa', 'VAP','QV_S', 'H', 'H_corr']
            
    df_FLUXNET = df_FLUXNET.resample('H').mean()
        
    return df_FLUXNET, st_name4plot       
              
# end def fluxnet_data
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine: euronet_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual EURONET data
# 
# Input parameters : main_path         - general path for research project
#                    sf_path           - name of subfolder for FLUXNET data    
#                    st_in     - the actual name of meteorologicl station
#
# Output parameters: df_euronet - the data frame with information about EURONET data
#------------------------------------------------------------------------------
def euronet_data(sf_path, st_in ):
       
    # Correction of years depends on the meteostation 
    if st_in in ('RuR','RuS'):
        year_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']  
    else:
        year_list = ['2007', '2008', '2009', '2010'] 
    
    # Create a correct name:
    euronet = []
    for year in year_list:
        f_name = f'EFDC_L2_Flx_DE{st_in}_{year}.txt'
        path   = f'{sf_path}{st_in}/{f_name}'
        data =  pd.read_csv(path, skiprows = 0, sep=',', parse_dates = {'Date':[0]},
                            header = 0, index_col = 0, skipinitialspace = True, 
                            na_values = ['-9999'])
            
        euronet.append(data)        
    
    df = pd.concat(euronet)    
    df = df.drop(['TIMESTAMP_END', 'DTime'], axis=1)
    df = df.resample('H').mean()
    df = df.dropna(how='any', axis=0, thresh=3 )

    return df

# end def euronet_data
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# Subroutines: montly_data, daily_data, hourly_data 
#------------------------------------------------------------------------------
#   
# The subroutines needs for getting timeseries values based on mean FLUXNET
# EURONET or GLEAM values
# 
#       montly_data ---> mean values by month (climatic mean - annual cycles) 
#       daily_data  ---> mean daily values by days for one June
#       hourly_data ---> mean hourly data (duirnal cycle)
#         
# Input parameters : data     - COSMO data
#                    period   - timeperiod for analysis
#                    ts       - timestep for resampling
#                    t1, t2   - dates for period
#                    dataset  - name of datasent      
#------------------------------------------------------------------------------
def montly_data(data, period, ts):
    m_data = data[period].resample(ts).mean()
    m_data = m_data.reset_index()
    num_id = m_data['index'].dt.month
    data_m = m_data.groupby(num_id).mean()
    # Re-indexing
    time_index = pd.date_range('1/1/2019', '12/1/2019', freq='MS').strftime('%B')
    data_m.index  = time_index
    return data_m


def daily_data(data, dataset, t_1, t_2, ts):   
    list_data = [] 
    for  tr in range(len(t_1)):
        # Get a time period
        if dataset in ('GLEAM', 'HYRAS'):
            period = pd.date_range(t_1[tr], t_2[tr], freq = 'D')
        else:
            period = pd.date_range(t_1[tr], t_2[tr], freq = '1H')       
              
        d_data   = data[period].resample(ts).mean()  
        list_data.append(d_data)    
    # Concat all year in on dataframe
    data_d = pd.concat(list_data, axis = 1)
            
    # Reset index
    data_d = data_d.reset_index()
    # Get day index in June 
    d_id    = data_d['index'].dt.day    
    data_d = data_d.groupby(d_id).mean()
    data_d = data_d.mean(axis = 1)   
    return data_d



def hourly_data(t_1h, t_2h, data):
    list_data = [] 
    for  tr in range(len(t_1h)):
        period = pd.date_range(t_1h[tr], t_2h[tr], freq = '1H')                                 
        d_data = data[period]  
        list_data.append(d_data)          
    # Concat all year in on dataframe
    data_d = pd.concat(list_data, axis = 1)    
    # Reset index
    data_d = data_d.reset_index()  
    # Get day index in June 
    d_id    = data_d['index'].dt.hour        
    data_d = data_d.groupby(d_id).mean()
    data_d = data_d.mean(axis = 1) 
    return data_d









def data4month(data, dataset, t_1, t_2, ts):   
    list_data = [] 
    for  tr in range(len(t_1)):
        # Get a time period
        if dataset in ('GLEAM', 'HYRAS'):
            period = pd.date_range(t_1[tr], t_2[tr], freq = 'D')
        else:
            period = pd.date_range(t_1[tr], t_2[tr], freq = '1H')       
              
        d_data   = data[period].resample(ts).mean()  
        list_data.append(d_data)    
    # Concat all year in on dataframe
    data_d = pd.concat(list_data, axis = 0)
            
    # Reset index
    data_d = data_d.reset_index()
    return(data_d)






















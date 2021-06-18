# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:13:33 2021

@author: churiulin
"""


import pandas as pd
import numpy as np
import sys



#------------------------------------------------------------------------------
# Subroutine: data_path
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual file name of FLUXNET data
#
# 
# Input parameters : meteo_station - name of meteorological station 
#                    f_name        - the actual version of data (FULLSET or ERAI) 
#                    tsep          - timestep (HH, DD, WW, MM, YY) 
#                    date_p        - timeperiod of data
#
#
# Output parameters: fN - the new file name 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def data_path(meteo_station, f_name, tstep, date_p):
    if tstep == 'HH':
        fN = 'FLX_DE-' + meteo_station + '_FLUXNET2015_' + f_name + '_' + tstep + '_' + date_p + '_1-4.csv'
    elif tstep == 'DD':
        fN = 'FLX_DE-' + meteo_station + '_FLUXNET2015_' + f_name + '_' + tstep + '_' + date_p + '_1-4.csv'
    elif tstep == 'WW':
        fN = 'FLX_DE-' + meteo_station + '_FLUXNET2015_' + f_name + '_' + tstep + '_' + date_p + '_1-4.csv'
    elif tstep == 'MM':
        fN = 'FLX_DE-' + meteo_station + '_FLUXNET2015_' + f_name + '_' + tstep + '_' + date_p + '_1-4.csv'
    elif tstep == 'YY':
        fN = 'FLX_DE-' + meteo_station + '_FLUXNET2015_' + f_name + '_' + tstep + '_' + date_p + '_1-4.csv'         
    else:
        print ('Incorrect timestep for FLUXNET data \n')
        sys.exit()       

    return fN

# end def data_path
#------------------------------------------------------------------------------





#------------------------------------------------------------------------------
# Subroutine: fluxnet_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual FLUXNET data
#
# 
# Input parameters : main_path         - general path for research project
#                    sf_path           - name of subfolder for FLUXNET data
#                    mode              - the type of FLUXNET data (FULLSET or ERAI)       
#                    mylist            - the list of meteorological station
#                    input_station     - the actual name of meteorologicl station
#
#
# Output parameters: df_fluxnet - the data frame with information about fluxnet data
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 05.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------


def fluxnet_data(main_path, sf_path, mode, mylist, input_station):
    
    # Main path
    mf_com   = main_path
    # Folder name (path)
    sf_fluxnet = sf_path
    # mode: FULLSET or ERAI
    input_mode = str(mode)


    #--------------------------------------------------------------------------
    # Path for FLUXNET data 
    #--------------------------------------------------------------------------
    

    #print (input_station)
    if input_mode == 'FULLSET':
        fullset_name = 'FULLSET'    
        if input_station  == 'RuR':
            input_date_start  = '2011'                                         # for RuR    
            input_date_end    = '2014'                                         # for RuR
            station_name_plot = 'Rollesbroich'
        elif input_station  == 'RuS':
            input_date_start  = '2011'                                         # for RuS    
            input_date_end    = '2014'                                         # for RuS
            station_name_plot = 'Selhausen Juelich'        
        elif input_station == 'SeH':
            input_date_start  = '2007'                                         # for SeH    
            input_date_end    = '2010'                                         # for SeH
            station_name_plot = 'Selhausen'              
    elif input_mode == 'ERAI':
        fullset_name = 'ERAI'   
        if input_station == 'RuR':
            input_date_start  = '1989'                                         # for RuR   
            input_date_end    = '2014'                                         # for RuR
            station_name_plot = 'Rollesbroich'
        elif input_station == 'RuS':
            input_date_start  = '1989'                                         # for RuS    
            input_date_end    = '2014'                                         # for RuS
            station_name_plot = 'Selhausen Juelich' 
        elif input_station == 'SeH':
            input_date_start  = '1989'                                         # for SeH    
            input_date_end    = '2014'                                         # for SeH
            station_name_plot = 'Selhausen'              
    else:
         print ('Error: Incorrect version of FLUXNET data \n')
         sys.exit()    


    date_period = input_date_start + '-' + input_date_end   
    print('FLUXNET data period: ', date_period)
     
    #--------------------------------------------------------------------------
    # Section: Load hourly FLUXNET filename. Timestep ---> HH (for all options)
    #--------------------------------------------------------------------------
    if input_station in mylist:
        meteo_station = input_station
        ssf_station = 'FLX_DE-' + meteo_station + '/'
        timestep = 'HH'
        fileName = data_path(meteo_station, fullset_name, timestep, date_period)
    else:
        print ('Station there is not in current list: The correct station are RuR, RuS, SeH \n')
        sys.exit()    
    
    #--------------------------------------------------------------------------
    # Section: Create a path for FLUXNET data. Timestep ---> HH (for all options)
    #--------------------------------------------------------------------------
    iPath_fluxnet = mf_com + sf_fluxnet + ssf_station + fileName


    #--------------------------------------------------------------------------
    # Section: Load data from FLUXNET data
    #--------------------------------------------------------------------------
       
    df_fluxnet = pd.read_csv(iPath_fluxnet, skiprows = 0, sep=',', dayfirst = True,
                             parse_dates = True, index_col = [0], skipinitialspace = True, 
                             na_values= ['-9999','********'])
   
    
    if input_mode == 'FULLSET':
        df_fluxnet = df_fluxnet.drop(['TIMESTAMP_END'], axis=1)
        
        # Create a nan timeseries
        s_zero = pd.Series(np.nan, index = df_fluxnet.index)
        
        # TA_F_MDS - Air temperature, gapfilled using MDS method 
        try:
            s_t_2m_mds  = df_fluxnet['TA_F_MDS']     
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_t_2m_mds = df_fluxnet['TA_F']     
        
        # TS_F_MDS_1 - Soil temperature, gapfilled with MDS -  1 is shallowest
        try:
            s_ts_mds_1  = df_fluxnet['TS_F_MDS_1']   
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_ts_mds_1 = s_zero                  
        
        # LE_F_MDS - Latent heat flux, gapfilled using MDS method 
        try:
            s_le_mds    = df_fluxnet['LE_F_MDS']
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_le_mds = s_zero                  
        
        # LE_CORR - Latent heat flux, corrected LE_F_MDS by energy
        #           balance closure correction factor
        try:
            s_le_corr   = df_fluxnet['LE_CORR']
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_le_corr = s_zero              
        
        # RH - Relative humidity, range 0-100
        try:
            s_rh_mds    = df_fluxnet['RH']
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_rh_mds = s_zero              
        
        # VPD_F_MDS - Vapor Pressure Deficit, gapfilled using MDS
        try:    
            s_vpd_mds   = df_fluxnet['VPD_F']
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_vpd_mds = df_fluxnet['VPD_F']                   
        
        # PA - Atmospheric pressure [kPa]
        try:    
            s_pa_mds    = df_fluxnet['PA']                
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_pa_mds = df_fluxnet['PA_F']          

        try:    
            s_h_mds    = df_fluxnet['H_F_MDS']                
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_h_mds = s_zero
            
        try:    
            s_h_corr    = df_fluxnet['H_CORR']                
        except KeyError as error:
            print ( 'No data from FLUXNET: ', error )
            s_h_corr = s_zero
            
            
        #----------------------------------------------------------------------
        # Create a dataframe with zero values which is equal --->  -9999   
        #----------------------------------------------------------------------
        df_zero = pd.DataFrame(data = np.full((len(s_t_2m_mds), 2), -9999))
           
        # Get two data series for new series for specific humidity and vapor pressure
        s_vap_pres_fluxnet = pd.Series(df_zero[0].values, index = s_t_2m_mds.index, dtype = 'float')   
        s_qv_s_fluxnet    =  pd.Series(df_zero[1].values, index = s_t_2m_mds.index, dtype = 'float') 
              
        # Calculete values
        for rfn in range(len(s_t_2m_mds)):
            s_vap_pres_fluxnet[rfn] = 1000.0 * 461.5 * (s_t_2m_mds[rfn] + 273.15)
            s_qv_s_fluxnet[rfn]     = 0.622 * s_vap_pres_fluxnet[rfn] / (s_pa_mds[rfn] - (1 - 0.622) * s_vap_pres_fluxnet[rfn])
        

        #----------------------------------------------------------------------
        # Section: Create dataframe and resample it to hourly timestep   
        #----------------------------------------------------------------------       
        
        df_FLUXNET = pd.concat([s_t_2m_mds, s_ts_mds_1, s_le_mds, s_le_corr,
                                s_rh_mds, s_vpd_mds, s_pa_mds, s_vap_pres_fluxnet,
                                s_qv_s_fluxnet, s_h_mds, s_h_corr], axis = 1)
            
        df_FLUXNET.columns = ['T2m', 'Ts', 'LE', 'LE_corr', 
                              'RH', 'VPD','Pa', 'VAP','QV_S', 'H', 'H_corr']
            
        df_FLUXNET = df_FLUXNET.resample('H').mean()
        
        return df_FLUXNET, station_name_plot       
        

    elif input_mode == 'ERAI': 
        print ('The section is in preparation \n')
        
        

# end def fluxnet_data
#------------------------------------------------------------------------------







#------------------------------------------------------------------------------
# Subroutine: euronet_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual EURONET data
#
# 
# Input parameters : main_path         - general path for research project
#                    sf_path           - name of subfolder for FLUXNET data    
#                    input_station     - the actual name of meteorologicl station
#
#
# Output parameters: df_euronet - the data frame with information about EURONET data
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 08.03.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------



def euronet_data(main_path, sf_path, input_station ):
    # The main path
    mf_com = main_path
    
    # The subfolder name
    sf_euronet = sf_path
    
    # The main name of station
    meteo_station = input_station
    
    # The subsubfolder name
    ssf_data   = meteo_station + '/'
    
    
    # Correction of years depends on the meteostation 
    if meteo_station == 'RuR':
        year_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    elif meteo_station == 'RuS':
        year_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']    
    else:
        year_list = ['2007', '2008', '2009', '2010'] 
    
    
    # Create a correct name:
    fn_list = []
    for i in range(len(year_list)):
        f_name = 'EFDC_L2_Flx_DE' + meteo_station + '_' + year_list[i] + '.txt'
        fn_list.append(f_name)
        
    # Create a correct path for EURONET data
    iPath_euronet = []
    for j in range(len(year_list)):
        temp_path = mf_com + sf_euronet + ssf_data + fn_list[j]
        iPath_euronet.append(temp_path)
        
    # Create data frame with hour timestep    
    df_list = []
    for l in range(len(iPath_euronet)):
        data =  pd.read_csv(iPath_euronet[l], skiprows = 0, sep=',', parse_dates = {'Date':[0]},
                            header = 0, index_col = 0, skipinitialspace = True, 
                            na_values = ['-9999'])
            
        df_list.append(data)    
        
        df_euronet = pd.concat(df_list)    
        df_euronet = df_euronet.drop(['TIMESTAMP_END'], axis=1)
        df_euronet = df_euronet.resample('H').mean()

    return df_euronet

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
# 
# Input parameters : data     - COSMO data
#                    period   - timeperiod for analysis
#                    ts       - timestep for resampling
#                    t1, t2   - dates for period
#                    dataset  - name of datasent
#         
# Output parameters: dataframe - dataframe with mean parameters 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 31.05.2021
# email: evgenychur@uni-kassel.de
#
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


def daily_data(t_1, t_2, data, ts, dataset):
    
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

































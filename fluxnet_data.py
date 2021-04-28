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
                                s_qv_s_fluxnet], axis = 1)
            
        df_FLUXNET.columns = ['T2m', 'Ts', 'LE', 'LE_corr', 
                              'RH', 'VPD','Pa', 'VAP','QV_S']
            
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
# Subroutine: linden_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual data from LINDEN meteostation
#
# 
# Input parameters : main_path         - general path for research project
#                    sf_path           - name of subfolder for FLUXNET data    
#                    input_station     - the actual name of meteorologicl station
#
#
# Output parameters: df_Linden - the data frame with information about LINDEN data
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 09.03.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------



mf_com     = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'
sf_linden  = 'IN-SITU/LINDEN/'



station      = '_Giessen.xlsx'
station_soil = '_Giessen_Soil.xlsx'
meteo        = 'meteodaten'



# List with information about Eddy covariance data
station_list = ['EC4', 'EC5', 'EC6' ]
year_list    = ['2009', '2010', '2011']


# List with information about soil data

soil_year    = ['2009', '2009', '2010', '2011']


# List with information about meteodata
date_list    = ['2005', '2006', '2007']

"""
fileName   = []
fileName_s = []
for i in range(len(station_list)):
    # Eddy covariance part
    for j in range(len(year_list)):
        fn_ec   = station_list[i] + station 
        fileName.append(fn_ec)        
    # Soil data part 
    for j in range(len(soil_year)):
        fn_soil   = station_list[i] + station_soil 
        fileName_s.append(fn_soil)
"""    

fN_meteo = []
for i in range(len(date_list)):
    fn_st = meteo + date_list[i] + '.csv'
    fN_meteo.append(fn_st)    

# Meteo data part
iPath_meteo = []  
for m in range(len(fN_meteo)):
    path_m   = mf_com + sf_linden + fN_meteo[m]
    iPath_meteo.append(path_m)       

df_meteo = []
for m in range(len(iPath_meteo)):
    df = pd.read_csv(iPath_meteo[m], skiprows = 0, sep=';', parse_dates = {'Date':[0,1]},
                     header = 0, index_col = 0, skipinitialspace = True, 
                     na_values = ['9990','********','***','******'])
    df_meteo.append(df)  

df_meteo = pd.concat(df_meteo, axis = 1)      
   
  
        
          
    


"""
sheet_list      = []
sheet_list_soil = []
for i in range(len(station_list)):
    # Eddy covariance part
    for j in range(len(year_list)):
        excel_list = station_list[i] + '_' + year_list[j]
        sheet_list.append(excel_list)    
    # Soil data part    
    for j in range(len(soil_year)):
        if (j == 0):
            excel_list_soil = station_list[i] + '_' + soil_year[j] + '_1h'
        else:
            excel_list_soil = station_list[i] + '_' + soil_year[j]
        sheet_list_soil.append(excel_list_soil)


# Eddy covariance part    
iPath = []  
for j in range(len(fileName)):
    path   = mf_com + sf_linden + fileName[j]
    iPath.append(path)

# Soil data part
iPath_soil = []  
for p in range(len(fileName_s)):
    path_s   = mf_com + sf_linden + fileName_s[p]
    iPath_soil.append(path_s)



# Eddy covariance part 

df_list_EC4 = []
df_list_EC5 = []
df_list_EC6 = []
for p in range(len(iPath)):
    if (p >= 0 and p <= 2):
        df = pd.read_excel(iPath[p], sheet_name = sheet_list[p] , header = 0,  skiprows = [1, 2],
                           parse_dates = ['Date'], index_col = 0, na_values= ['NAN', '--', '-9999.9'])  
        
        df = df.resample('H').mean()
        
        df_list_EC4.append(df)
    elif (p >= 3 and p <=5):
        df = pd.read_excel(iPath[p], sheet_name = sheet_list[p] , header = 0,  skiprows = [1, 2],
                           parse_dates = ['Date'], index_col = 0, na_values= ['NAN', '--', '-9999.9'])  
        
        df = df.resample('H').mean()
        
        df_list_EC5.append(df)
    else:
        df = pd.read_excel(iPath[p], sheet_name = sheet_list[p] , header = 0,  skiprows = [1, 2],
                           parse_dates = ['Date'], index_col = 0, na_values= ['NAN', '--', '-9999.9'])  
        
        df = df.resample('H').mean()
        
        df_list_EC6.append(df)
        

df_linden_EC4 = pd.concat(df_list_EC4)
df_linden_EC4 = df_linden_EC4.drop(['Day of Year', 'Time'], axis=1)
     

df_linden_EC5 = pd.concat(df_list_EC5)
df_linden_EC5 = df_linden_EC5.drop(['Day of Year', 'Time'], axis=1)


df_linden_EC6 = pd.concat(df_list_EC6)
df_linden_EC6 = df_linden_EC6.drop(['Day of Year', 'Time'], axis=1)




# Soil data part
df_list_soil_EC4 = []
df_list_soil_EC5 = []
df_list_soil_EC6 = []
for s in range(len(iPath_soil)):
    if (s >= 0 and s <= 3):
        df_s = pd.read_excel(iPath_soil[s], sheet_name = sheet_list_soil[s] , header = 0,  skiprows = [1, 2, 3, 4],
                             parse_dates = ['Date'], index_col = 0, na_values= ['NAN', '--', '-9999.9'])  
    
        df_s = df_s.resample('H').mean()
        
        df_list_soil_EC4.append(df_s)  
        
    elif (s >= 4 and s <= 7):
        df_s = pd.read_excel(iPath_soil[s], sheet_name = sheet_list_soil[s] , header = 0,  skiprows = [1, 2, 3, 4],
                             parse_dates = ['Date'], index_col = 0, na_values= ['NAN', '--', '-9999.9'])  
        
        df_s = df_s.resample('H').mean()
        
        df_list_soil_EC5.append(df_s)         
    else:
        df_s = pd.read_excel(iPath_soil[s], sheet_name = sheet_list_soil[s] , header = 0,  skiprows = [1, 2, 3, 4],
                             parse_dates = ['Date'], index_col = 0, na_values= ['NAN', '--', '-9999.9'])  
    
        df_s = df_s.resample('H').mean()
        
        df_list_soil_EC6.append(df_s)         

    
    
df_linden_soil_EC4 = pd.concat(df_list_soil_EC4) 
df_linden_soil_EC4 = df_linden_soil_EC4.drop(['Day of Year', 'Time'], axis=1)
df_linden_soil_EC4 = df_linden_soil_EC4.rename(columns={'Soiltemp.'    :'TS_1', 'Soiltemp..1'  :'TS_2',
                                                        'Soiltemp..2'  :'TS_3', 'Soiltemp..3'  :'TS_4', 'Soiltemp..4'  :'TS_5',
                                                        'Volum. Soil'  :'VS_1', 'Volum. Soil.1':'VS_2',
                                                        'Volum. Soil.2':'VS_3', 'Volum. Soil.3':'WS_4',
                                                        'Volum. Soil.4':'WS_5', 'Ground heat'  :'G'   })
df_linden_soil_EC4 = df_linden_soil_EC4.drop(['TS_5', 'WS_5'], axis=1)



df_linden_soil_EC5 = pd.concat(df_list_soil_EC5)
df_linden_soil_EC5 = df_linden_soil_EC5.drop(['Day of Year', 'Time'], axis=1)
df_linden_soil_EC5 = df_linden_soil_EC5.rename(columns={'Soiltemp.'    :'TS_1', 'Soiltemp..1'  :'TS_2',
                                                        'Soiltemp..2'  :'TS_3', 'Soiltemp..3'  :'TS_4', 'Soiltemp..4'  :'TS_5',
                                                        'Volum. Soil'  :'VS_1', 'Volum. Soil.1':'VS_2',
                                                        'Volum. Soil.2':'VS_3', 'Volum. Soil.3':'WS_4',
                                                        'Volum. Soil.4':'WS_5', 'Ground heat'  :'G'   })
df_linden_soil_EC5 = df_linden_soil_EC5.drop(['TS_5', 'WS_5'], axis=1)


df_linden_soil_EC6 = pd.concat(df_list_soil_EC6) 
df_linden_soil_EC6 = df_linden_soil_EC6.drop(['Day of Year', 'Time'], axis=1)
df_linden_soil_EC6 = df_linden_soil_EC6.rename(columns={'Soiltemp.'    :'TS_1', 'Soiltemp..1'  :'TS_2',
                                                        'Soiltemp..2'  :'TS_3', 'Soiltemp..3'  :'TS_4', 'Soiltemp..4'  :'TS_5',
                                                        'Volum. Soil'  :'VS_1', 'Volum. Soil.1':'VS_2',
                                                        'Volum. Soil.2':'VS_3', 'Volum. Soil.3':'WS_4',
                                                        'Volum. Soil.4':'WS_5', 'Ground heat'  :'G'   })
df_linden_soil_EC6 = df_linden_soil_EC6.drop(['TS_5', 'WS_5'], axis=1)



"""








 



# end def linden_data
#------------------------------------------------------------------------------




















#------------------------------------------------------------------------------
# Subroutine: lindenberg_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual Lindenberg data
#
# 
# Input parameters : main_path         - general path for research project
#                    sf_path           - name of subfolder for FLUXNET data    
#                    input_station     - the actual name of meteorologicl station
#
#
# Output parameters: df_lindenberg - the data frame with information about Lindenberg data
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 09.03.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------












# end def lindenberg_data
#------------------------------------------------------------------------------
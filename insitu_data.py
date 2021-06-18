# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 09:56:44 2021

@author: churiulin
"""



import pandas as pd
import numpy as np
import sys




def get_data(mf_com, sf_lindenberg, fn_name):
    iPath = mf_com + sf_lindenberg + fn_name
    df = pd.read_csv(iPath, skiprows = 0, sep=';', dayfirst = True,
                     parse_dates = True, index_col = [0], skipinitialspace = True, 
                     na_values= ['-9999','********'])
    return df


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
"""

# Different options for data: 1 - addy covariance data
#                             2 - soil data  
#                             3 - meteo data

mode = 3

# Paths to input and output data
mf_com     = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'
sf_linden  = 'IN-SITU/INITIAL/LINDEN/'
path_exit  = mf_com + 'IN-SITU/LINDEN/'


# Constant names of excel files
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




#------------------------------------------------------------------------------
# Eddy covariance data - Linden
#------------------------------------------------------------------------------
if mode == 1:
    
    sheet_list  = [] # List for sheets of excel file
    iPath       = [] # List for paths for data 
    df_list_EC4 = [] # list for EC4 station
    df_list_EC5 = [] # list for EC5 station
    df_list_EC6 = [] # list for EC6 station
    
    
    for i in range(len(station_list)):
        for j in range(len(year_list)):
            # Define file name
            fn_ec   = station_list[i] + station 
            # Define path to soil data            
            path   = mf_com + sf_linden + fn_ec
            # Define excel sheet
            excel_list = station_list[i] + '_' + year_list[j]
            # Add values to lists
            iPath.append(path)  
            sheet_list.append(excel_list) 
      
            
    # The main calculations
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
           
    # Export to EXCEL
    df_linden_EC4.to_csv(path_exit  + 'EC4.csv', sep = ';', float_format='%.3f') 
    df_linden_EC5.to_csv(path_exit  + 'EC5.csv', sep = ';', float_format='%.3f') 
    df_linden_EC6.to_csv(path_exit  + 'EC6.csv', sep = ';', float_format='%.3f') 
    
#------------------------------------------------------------------------------
# Soil data - linden
#------------------------------------------------------------------------------
elif mode == 2:
    
    sheet_list_soil  = [] # List for sheets of excel file
    iPath_soil       = [] # List for paths for data 
    df_list_soil_EC4 = [] # list for EC4 station
    df_list_soil_EC5 = [] # list for EC5 station
    df_list_soil_EC6 = [] # list for EC6 station
    
    for i in range(len(station_list)):    
        for j in range(len(soil_year)):
            # Define soil name
            fn_soil  = station_list[i] + station_soil
            # Define path to soil data
            path_s   = mf_com + sf_linden + fn_soil
                       
            # Define sheets name
            if (j == 0):
                excel_list_soil = station_list[i] + '_' + soil_year[j] + '_1h'
            else:
                excel_list_soil = station_list[i] + '_' + soil_year[j]        
            
            # Add values to our lists
            iPath_soil.append(path_s)
            sheet_list_soil.append(excel_list_soil)
    
           
    # The main calculations
    for s in range(len(iPath_soil)):
        if (s >= 0 and s <= 3):
            df_s = pd.read_excel(iPath_soil[s], sheet_name = sheet_list_soil[s] ,    header = 0,
                                 skiprows = [1, 2, 3, 4], parse_dates = ['Date'], index_col = 0, 
                                 na_values= ['NAN', '--', '-9999.9'])  
        
            df_s = df_s.resample('H').mean()
            
            df_list_soil_EC4.append(df_s)  
            
        elif (s >= 4 and s <= 7):
            df_s = pd.read_excel(iPath_soil[s], sheet_name = sheet_list_soil[s] ,    header = 0, 
                                 skiprows = [1, 2, 3, 4], parse_dates = ['Date'], index_col = 0, 
                                 na_values= ['NAN', '--', '-9999.9'])  
            
            df_s = df_s.resample('H').mean()
            
            df_list_soil_EC5.append(df_s)         
        else:
            df_s = pd.read_excel(iPath_soil[s], sheet_name = sheet_list_soil[s] ,    header = 0,  
                                 skiprows = [1, 2, 3, 4], parse_dates = ['Date'], index_col = 0,
                                 na_values= ['NAN', '--', '-9999.9'])  
        
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
        

    df_linden_soil_EC4.to_csv(path_exit  + 'EC4_soil.csv', sep = ';', float_format='%.3f') 
    df_linden_soil_EC5.to_csv(path_exit  + 'EC5_soil.csv', sep = ';', float_format='%.3f') 
    df_linden_soil_EC6.to_csv(path_exit  + 'EC6_soil.csv', sep = ';', float_format='%.3f') 

#------------------------------------------------------------------------------
# Meteorological data - Linden
#------------------------------------------------------------------------------
elif mode == 3:
    
    iPath_meteo = []
    df_meteo    = []


    for i in range(len(date_list)):
        fn_st  = meteo  + date_list[i] + '.csv'
        path_m = mf_com + sf_linden    + fn_st
        iPath_meteo.append(path_m)       
    
    
    for m in range(len(iPath_meteo)):
        df = pd.read_csv(iPath_meteo[m], skiprows = 0, sep=';', parse_dates = {'Date':[0,1]},
                         header = 0, index_col = 0, skipinitialspace = True, 
                         na_values = ['9990','********','***','******'])
        df_meteo.append(df)  
    
    df_meteo = pd.concat(df_meteo, axis = 0)      
   
    df_meteo.to_csv(path_exit  + 'Meteo_linden.csv', float_format='%.3f') 
        
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

"""
def get_index(df):

    time_period = df.iloc[:,0].astype(str)
        
    year  = pd.Series(np.nan, index = range(len(time_period)))
    month = pd.Series(np.nan, index = range(len(time_period)))
    day   = pd.Series(np.nan, index = range(len(time_period)))
    hour  = pd.Series(np.nan, index = range(len(time_period)))
    
    for i in range(len(time_period)):
        year[i]  = time_period[i][0:4]
        month[i] = time_period[i][4:6]
        day[i]   = time_period[i][6:8]
        hour[i]  = time_period[i][8:10]
    
    
    year  = year.astype(int)
    month = month.astype(int)
    day   = day.astype(int)
    hour  = hour.astype(int)
    
    
    dates = [pd.to_datetime('{}-{}-{}-{}'.format(i, j, z, k), format='%Y-%m-%d-%H') for i,j,z,k in zip(year, month, day, hour)] 

    return dates



# Paths to input and output data
mf_com         = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'
sf_lindenberg  = 'IN-SITU/INITIAL/LINDENBERG/'
path_exit      = mf_com + 'IN-SITU/LINDENBERG/'


# Constant names of excel files
fN1 = 'sups_rao_mett01mets_l1_anypa_v00_2000_2020.txt'
fN2 = 'sups_rao_turb00_l2_any_v00_2002_2016.txt'
fN3 = 'sups_rao_turb00_l2_any_v00_2016_2020.txt'


iPath1 = mf_com + sf_lindenberg + fN1
iPath2 = mf_com + sf_lindenberg + fN2
iPath3 = mf_com + sf_lindenberg + fN3



df1 = pd.read_csv(iPath1, skiprows = 0, sep=';', header = 0, skipinitialspace = True,
                  na_values = ['-9999','********','***','******'])
                  
                  #parse_dates = {'Date':[0,1]},
 
df2 = pd.read_csv(iPath2, skiprows = 0, sep=';', header = 0, skipinitialspace = True,
                  na_values = ['-9999','********','***','******'])
                          


df3 = pd.read_csv(iPath3, skiprows = 0, sep=';', header = 0, skipinitialspace = True,
                  na_values = ['-9999','********','***','******'])                          




index_df1 = get_index(df1)
index_df2 = get_index(df2)
index_df3 = get_index(df3)



t2m = pd.Series(df1['TAIR002'].values, index = index_df1)
rh  = pd.Series(df1['RH002'].values  , index = index_df1)
qv  = pd.Series(df1['QV002'].values  , index = index_df1)
ps  = pd.Series(df1['PS'].values     , index = index_df1)

# ss sensible heat
# ls latent heat
# et evapotranspiration

lh_1 = pd.Series(df2['HFLS'].values, index = index_df2).resample('1H').mean() 
sh_1 = pd.Series(df2['HFSS'].values, index = index_df2).resample('1H').mean() 

lh_2 = pd.Series(df3['HFLS'].values, index = index_df3).resample('1H').mean() 
sh_2 = pd.Series(df3['HFSS'].values, index = index_df3).resample('1H').mean() 
et   = pd.Series(df3['ET'].values  , index = index_df3).resample('1H').mean() 

lh = pd.concat([lh_1, lh_2], axis = 0)
sh = pd.concat([sh_1, sh_2], axis = 0)



df_lindenberg = pd.concat([t2m, rh, qv, ps, 
                           lh_1, lh_2, 
                           sh_1, sh_2, et ], axis = 1)


# Rename columnsin dataframe with observations
df_lindenberg.columns = ['T_2M', 'RH', 'QV', 'PS', 
                         'LHFL_1', 'LHFL_2',
                         'SHFL_1', 'LHFL_2', 'ZVERBO']


#df_lindenberg.to_excel(path_exit  + 'Lindenberg.xlsx', float_format='%.3f') 
df_lindenberg.to_csv(path_exit  + 'Lindenberg.csv', sep = ';', float_format='%.3f') 
# end def lindenberg_data
#------------------------------------------------------------------------------
"""



def montly_data(data, period, ts):
    m_data = data[period].resample(ts).mean()
    m_data = m_data.reset_index()
    num_id = m_data['Date'].dt.month
    data_m = m_data.groupby(num_id).mean()

    # Re-indexing
    time_index = pd.date_range('1/1/2019', '12/1/2019', freq='MS').strftime('%B')
    data_m.index  = time_index

    return data_m

 
       # m_lh = df_in_situ['LatHeat'].resample('1H').mean()
       # m_lh = m_lh.reset_index()
        
       #  num_id = m_lh['Date'].dt.month
       # lh_m = m_lh.groupby(num_id).mean()
        
        # Re-indexing
      #  time_index = pd.date_range('1/1/2019', '12/1/2019', freq='MS').strftime('%B')
       # lh_m.index  = time_index
   
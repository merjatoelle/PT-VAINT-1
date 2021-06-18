# -*- coding: utf-8 -*-
"""
The insitu_data is the main programm for preparing data based on an initial 
information from Linden and Lindenberg stations, moreover module contains
several subrutines for statistical analysis
                                   
The progam contains several subroutines for:
    
    get_index ---> Get time index for Linden and Lindenberg data
    stat_temp ---> statistical analysis of data
    
Moreover, you can use this module for preparing Linden and Lindenberg data based
on sites original information. For this option you can parameters calc with
values 'yes' or 'no'

In case of - YES the two subrutines will be work:
    linden_data     ---> prepare dataframe with Lindenberg data
    lindenberg_data ---> prepare dataframe with Lindenberg data
In case of - NO, you can see the phrase:
    "The initial data are not needed"

                                                
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

# Import standart liblaries 
import sys
import numpy as np
import pandas as pd

# Improt methods for statistical analysis
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

#------------------------------------------------------------------------------
# Subroutine: get_index
#------------------------------------------------------------------------------
#
# The subroutine needs for creation of timeindex based on data from the first
# column of Linden and Lindenberg data
# 
# Input parameters : df - the Linden or Lindenberg data                     
#------------------------------------------------------------------------------

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


#------------------------------------------------------------------------------
# Subroutine: stat_tepm
#------------------------------------------------------------------------------
#
# The subroutine needs for statistical analysis of COSMO data to compare with 
# Linden and Lindenberg data
# 
# Input parameters : df_model - the model dataset
#                    ts_obs   - the timeseries with in-situ data   
#                    name     - the name of research parameter
#------------------------------------------------------------------------------
def stat_tepm(df_model, ts_obs, name):
    #stat_data = pd.concat([df_cosmo_orig['T_2M'], t2m], axis = 1)
    stat_data = pd.concat([df_model, ts_obs], axis = 1)
    stat_data.columns = ['MOD', 'OBS']
    stat_data = stat_data.dropna()

    mean_obs = stat_data['OBS'].mean()
    max_obs  = stat_data['OBS'].max()
    min_obs  = stat_data['OBS'].min()
    std_obs  = stat_data['OBS'].std() 
    mean_mod = stat_data['MOD'].mean()
    max_mod  = stat_data['MOD'].max()
    min_mod  = stat_data['MOD'].min()
    std_mod  = stat_data['MOD'].std()      
    mae      = mean_absolute_error(stat_data['OBS'], stat_data['MOD'])
    rmse     = mean_squared_error(stat_data['OBS'], stat_data['MOD'])
    corr     = stat_data['OBS'].corr(stat_data['MOD'])

    df_stat = pd.DataFrame({'Parameter' : [name],
                              'Mean OBS': mean_obs,
                              'Mean MOD': mean_mod,
                              'Max OBS' : max_obs ,
                              'Max MOD' : max_mod ,
                              'Min OBS' : min_obs ,
                              'Min MOD' : min_mod ,
                              'STD OBS' : std_obs ,
                              'STD_MOD' : std_mod ,
                                  'MAE' : mae     ,
                                 'RMSE' : rmse    ,
                                 'CORR' : corr    })

    df_stat.set_index('Parameter', inplace = True)

    return df_stat
# End of stat_temp
#------------------------------------------------------------------------------






# Do you want to prepare an initial Linden and Lindenberg data
calc = 'yes' # No




if calc == 'yes':
    #--------------------------------------------------------------------------
    # Subroutine: linden_data
    #--------------------------------------------------------------------------
    #
    # The subroutine needs for getting actual data from LINDEN meteostation
    #--------------------------------------------------------------------------
    
    
    # Different options for data: 1 - addy covariance data
    #                             2 - soil data  
    #                             3 - meteo data
    
    mode = 3
    
    # Paths to input and output data
    mf_com         = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'
    # subfolders paths
    sf_linden      = 'IN-SITU/INITIAL/LINDEN/'
    sf_lindenberg  = 'IN-SITU/INITIAL/LINDENBERG/'
    # Output paths
    path_exit      = mf_com + 'IN-SITU/LINDEN/'
    path_exit2     = mf_com + 'IN-SITU/LINDENBERG/'
    

    # Constant names of files for Linden data
    station      = '_Giessen.xlsx'
    station_soil = '_Giessen_Soil.xlsx'
    meteo        = 'meteodaten'
            
    # Constant names of files for Lindenberg data
    fN1 = 'sups_rao_mett01mets_l1_anypa_v00_2000_2020.txt'
    fN2 = 'sups_rao_turb00_l2_any_v00_2002_2016.txt'
    fN3 = 'sups_rao_turb00_l2_any_v00_2016_2020.txt'
            
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
                    
    # end Linden_data
    #--------------------------------------------------------------------------


    #--------------------------------------------------------------------------
    # Subroutine: lindenberg_data
    #--------------------------------------------------------------------------
    # The subroutine needs for getting actual Lindenberg data
    #--------------------------------------------------------------------------
   
    
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
    df_lindenberg.to_csv(path_exit2  + 'Lindenberg.csv', sep = ';', float_format='%.3f') 
    
    # end def lindenberg_data
    #------------------------------------------------------------------------------

else:
    print('The initial data are not needed')






   
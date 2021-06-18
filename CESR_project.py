# -*- coding: utf-8 -*-
"""
The CESR_project is the main program for data analysis and visualization of PT VAINT.

The progam contains several additional modules:
    cosmo_data       ---> module for downloading and preparing COSMO data
    fluxnet_data     ---> module for downloading and preparing FLUXNET and EURONET data
    insitu_data      ---> module for downloading and preparing data from Linden and Lindenberg
    reanalysis_data  ---> module for downloading and preparing reanalysis data from E-OBS, HYRAS and GLEAM datasets
    system_operation ---> module with a system functions for cleaning data
    vis_module       ---> module for data visualization
    
    
Autors of project: Evgenii Churiulin, Merja Tölle, Center for Enviromental System
                                                   Research (CESR) 

                                                   
Acknowledgements: Vladimir Kopeikin, Denis Blinov



Current Code Owner: CESR, Evgenii Churiulin
phone:  +49  561 804-6142
fax:    +49  561 804-6116
email:  evgenychur@uni-kassel.de


History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    2021-04-15 Evgenii Churiulin, Center for Enviromental System Research (CESR)
           Initial release
                 

"""
# Import standart liblaries 
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import personal libraries
import vis_module       as vis                                                 
import reanalysis_data  as radata                                              
import fluxnet_data     as flnt                                                             
import cosmo_data       as csm_data                                            
import system_operation as stmo                                                


# Start programm

#------------------------------------------------------------------------------
# Section for logical data types ----> Don't change them
#------------------------------------------------------------------------------

# Logucal types for actual timesteps (There is an option for work with
#                                     hour  data timestep - ldaily,
#                                     daily data timestep - lperiod,
#                                     user  data timestep - llperiod)

ldaily   = True                                                                
lperiod  = True                                                                
llperiod = True                                                                

# Logical types for GLEAM data (version a - v3.5a, 
#                               version b - v.3.5b, 
#                               version bt - both version together)
version_a       = True                                                         
version_b       = True                                                         
version_bt      = True                                                         
#End of section
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Section: Constant parameters
#------------------------------------------------------------------------------
t0melt = 273.15                                                                

#End of section
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# Section for users: Parameters can be changed by user
#------------------------------------------------------------------------------             
#
# mf_com ---> The main paths which are general for all data
# sf     ---> subfolder
# ssf    ---> subsubfolder
# sssf   ---> subsubsubfolder 
#------------------------------------------------------------------------------                           

mf_com    = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'

# path for results
path_exit = mf_com + 'Python_results/'

#------------------------------------------------------------------------------
# Subfolders for model data
#------------------------------------------------------------------------------
sf_parc01_ctr     = 'COSMO/PARC/CTR/'                                          # COSMO_CTR
sf_parc_v35       = 'COSMO/PARC/v3.5/'                                         # COSMO_v3.5
sf_parc_v45       = 'COSMO/PARC/v4.5/'                                         # COSMO_v4.5
sf_parc_v45_evap  = 'COSMO/PARC/v4.5e/'                                        # COSMO_v4.5e

#------------------------------------------------------------------------------
# Subfolder for IN-SITU data
#------------------------------------------------------------------------------
sf_fluxnet    = 'IN-SITU/FLUXNET/'                                             # FLUXNET data    
sf_euronet    = 'IN-SITU/EURONET/'                                             # EURONET data
sf_linden     = 'IN-SITU/LINDEN/'                                              # Linden  data 
sf_lindenberg = 'IN-SITU/LINDENBERG/'                                          # Lindenberg  data 

#------------------------------------------------------------------------------
# Subfolders for REANALYSIS data                                                     
#------------------------------------------------------------------------------
sf_eobs    = 'REANALYSIS/EOBS/'                                                # EOBS data
sf_hyras   = 'REANALYSIS/HYRAS/'                                               # HYRAS data
sf_gleam   = 'REANALYSIS/GLEAM/'                                               # GLEAM data  

#------------------------------------------------------------------------------
# Subsubfolders for model results
#------------------------------------------------------------------------------
ssf_cosmo = ['AEVAP_S/'  , 'ALHFL_BS/' , 'ALHFL_PL/', 'ALHFL_S/' , 'ASHFL_S/',
             'ZTRALEAV/' , 'ZTRANG/'   , 'ZTRANGS/' , 'ZVERBO/'  , 'QV_2M/'  , 
             'QV_S/'     , 'RELHUM_2M/', 'RSTOM/'   , 'T_2M/'    , 'T_S/'    ,
             'PS/'       ]
#------------------------------------------------------------------------------ 
# Names of parameters for COSMO data
#------------------------------------------------------------------------------
clm_name = ['AEVAP_S'  , 'ALHFL_BS' , 'ALHFL_PL', 'ALHFL_S' , 'ASHFL_S', 
            'ZTRALEAV' , 'ZTRANG'   , 'ZTRANGS' , 'ZVERBO'  , 'QV_2M'  , 
            'QV_S'     , 'RELHUM_2M', 'RSTOM'   , 'T_2M'    , 'T_S'    ,
            'PS'       ]


#------------------------------------------------------------------------------
# General part in file name for COSMO and experiments (fn - fileName)
#------------------------------------------------------------------------------
fn_cosmo = '_ts_mean_1999_2015.csv'

#------------------------------------------------------------------------------
# EURONET or FLUXNET stations for work
#------------------------------------------------------------------------------
mylist = ['RuR', 'RuS', 'SeH']

#------------------------------------------------------------------------------
# Parameters for: period_cal    --> timestep of data (1 - hourly, 
#                                                     2 - Montly,
#                                                     3 - User interval)
#
#                 f_GLEAM_data  --> version of GLEAM data (A - 3.5a;
#                                                          B - 3.5b,
#                                                          BT - both)
#    
#                 f_region      --> (P - park,
#                                    L - linden,
#                                    Li - lindenberg)
# 
#                 f_station     --> (For Park region --> RuR --> 'Rollesbroich      (lat - 50.62; lon - 6.30; Land type - Grass)
#                                                        RuS --> 'Selhausen Juelich (lat - 50.86; lon - 6.44; Land type - Crops) 
#                                                        SeH --> 'Selhausen         (lat - 50.87; lon - 6.44; Land type - Agricultural area)
#                                    For Linden      --> LiN --> 'Linden'           (lat - ; lon - ; Land type - Grass)
#                                    For Lindenberg  --> LiD --> 'Lindenberg'       (lat - ; lon - ; Land type - ))
#           
#                 time_array   --> time step for resample initial dataframe
#                                  if period_cal = 1 then time_array = 'H'
#                                     period_cal = 2 then time_array = 'D'
#                                     period_cal = 3 then time_array = '2D'   
#------------------------------------------------------------------------------
period_cal   = '3'           
f_GLEAM_data = 'BT'         
f_region     = 'P'
f_station    = 'RuR'           
time_array   = ['H', 'D', '2D']

# Types of parameters for analysis (HYRAS)
parameters = ['T_2M', 'T_MAX', 'T_MIN', 'T_S']

#------------------------------------------------------------------------------
# Version of FLUXNET data: ERAI or FULLSET
#------------------------------------------------------------------------------
input_mode = 'FULLSET'

#------------------------------------------------------------------------------
# Names of plot labels
#------------------------------------------------------------------------------
name_1 = ['Amount of water evaporation (surface) - AEVAP_S'                ,
          'Average latent heat flux from bare soil evaporation - ALHFL_BS' ,
          'Average latent heat flux from plants - ALHFL_PL'                ,
          'Average latent heat flux (surface) - ALHFL_S'                   ,
          'Average sensible heat flux (surface) - ASHFL_S'                 ,
          'Average transpiration rate of dry leaves - AZTRALEAV'           ,
          'Average transpiration contribution by the first layer - AZTRANG',
          'Average total transpiration - AZTRANGS'                         ,
          'Average total evapotranspiration - AZVERBO'                     , 
          'Specific_humidity in 2m - QV_2M'                                ,
          'Surface_specific_humidity - QV_S'                               ,
          'Relative_humidity  in 2m - RELHUM_2M'                           ,
          'Stomata resistance - RSTOM'                                     , 
          'Air temperature  in 2m - T_2M'                                  ,
          'Soil temperature  in 2m - T_S'                                  ,  
          'Surface pressure - PS'                                          ]         
          

#------------------------------------------------------------------------------
# Names of y axis
#------------------------------------------------------------------------------                                         
name_2 = ['AEVAP_S, kg/m2' , 'ALHFL_BS, W/m2'  , 'ALHFL_PL, W/m2' ,
          'ALHFL_S, W/m2'  , 'ASHFL_S, W/m2'   , 'ZTRALEAV'       , 
          'ZTRANG'         , 'ZTRANGS'         , 'ZVERBO, mm/day' ,
          'QV_2M, kg/kg'   , 'QV_S, kg/kg'     , 'RELHUM_2M, %'   , 
          'RSTOM, s/m'     , 'T_2M, C'         , 'T_S, C'         ,
          'PS, hPa'            ]
          
#------------------------------------------------------------------------------    
# Names of plots --> for controlling  
#------------------------------------------------------------------------------    
plot_name = ['Plot - AEVAP_S'  , 'Plot - ALHFL_BS' , 'Plot - ALHFL_PL' , 
             'Plot - ALHFL_S'  , 'Plot - ASHFL_S'  , 'Plot - ZTRALEAV' ,
             'Plot - ZTRANG'   , 'Plot - ZTRANGS'  , 'Plot - ZVERBO'   , 
             'Plot - QV_2M'    , 'Plot - QV_S'     , 'Plot - RELHUM_2M',
             'Plot - RSTOM'    , 'Plot - T_2M'     , 'Plot - T_S'      ,
             'Plot - PS'       ]

  
#------------------------------------------------------------------------------
# Range of values for parameters.  m - monthly; u - user;
# -----------------------------------------------------------------------------

# DAILY data with hourly timesteps
#            AEVAP, ALHFL_BS, ALHFL_PL, ALHFL_S ,  ASHFL_S, AZTRALEAV, AZTRANG, AZTRANGS, AZVERBO, QV_2M ,   QV_S, RELHUM_2M,   RSTOM,  T_2M,   T_S,  PS 
y_min_d  = [ -0.05,     -5.0,     -5.0,    -25.0,      0.0,       0.0,     0.0,      0.0,     0.0, 0.0   ,   -2.0,      30.0,     0.0, -15.0, -15.0, 900.0 ]
y_max_d  = [  0.41,     50.1,     50.1,    250.1,    250.1,      50.1,    50.1,     50.1,    50.0, 0.0151,   2.01,     100.1,  5001.0,  35.1,  35.0, 1050.1]
y_step_d = [  0.05,      5.0,      5.0,     25.0,     25.0,      10.0,    10.0,     10.0,    10.0, 0.005 ,    0.5,      10.0,   500.0,  10.0,  10.0, 25.0  ]

# MONTLY data with daily timesteps
#            AEVAP, ALHFL_BS, ALHFL_PL, ALHFL_S ,  ASHFL_S, AZTRALEAV, AZTRANG, AZTRANGS, AZVERBO, QV_2M ,   QV_S, RELHUM_2M,   RSTOM,  T_2M,   T_S,  PS 
y_min_m  = [  0.0 ,    -25.0,    -25.0,    -25.0,      0.0,       0.0,     0.0,     0.0,      0.0, 0.0   ,    0.0,      30.0,     0.0, -15.0, -15.0, 900.0 ]
y_max_m  = [  6.01,    125.1,    125.1,    125.1,    250.1,      50.1,    50.1,    50.1,     50.1, 0.0151, 0.0151,     100.1, 20000.1,  35.1,  35.0, 1050.1]
y_step_m = [  0.50,     25.0,     25.0,     25.0,     25.0,      10.0,    10.0,    10.0,     10.0, 0.005 ,  0.005,      10.0,  5000.0,  10.0,  10.0, 25.0  ]

# USER data with user timesteps
#            AEVAP, ALHFL_BS, ALHFL_PL, ALHFL_S,  ASHFL_S, AZTRALEAV, AZTRANG, AZTRANGS, AZVERBO, QV_2M ,    QV_S, RELHUM_2M,   RSTOM,  T_2M,   T_S,  PS 
y_min_u  = [   0.0,      0.0,      0.0,     0.0,   -100.0,       0.0,       0.0,     0.0,     0.0,  0.0   ,    0.0,       30.0,     0.0, -15.0, -15.0, 900.0 ]
y_max_u  = [ 10.01,    125.1,     50.1,   125.1,    125.1,      10.1,      10.0,    10.0,    10.1,  0.0151, 0.0151,      100.1,  40000.1,  35.1,  35.0, 1050.1]
y_step_u = [   2.0,     25.0,      5.0,    25.0,     25.0,       2.0,       2.0,     2.0,     1.0,  0.005 ,  0.005,       10.0,   5000.0,  10.0,  10.0, 25.0  ]            


#End of section
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Section: Paths for results
#------------------------------------------------------------------------------

# Results paths
result_path = []
for cl in range(len(ssf_cosmo)):
    path_to_result = path_exit + ssf_cosmo[cl]
    result_path.append(path_to_result)
    
#End of section
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# Section: Clear the privios results
#------------------------------------------------------------------------------

while True:
    input_control = input('Do you want to remote previous data: yes - y; no - n \n') 
    if input_control == 'y':
        for cln in range(len(result_path)):
            clean_result = stmo.dep_clean(result_path[cln])
        print ('All previous results were deleted: \n')        
        break
    elif input_control == 'n': 
        print ('All previous results were saved and ' +
               'in case of the same name - data will be rewritten: \n')
        break
    else:
        print ('Error: Incorrect format, repeat! \n')

#End of section
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Select actual period and time step for data: 1 - Daily with hourly time step
#                                              2 - Montly with daily time step
#                                              3 - Users  with 2 days time step     
#------------------------------------------------------------------------------
#print('Choose the period for work: 1 - Daily; 2 - Montly; 3 - User; \n')
#input_type = input()
input_type = period_cal

if input_type == '1':                                                         
    daily_time_step   = True                                                   
    monthly_time_step = False     
    long_time_step    = False 
    ts = time_array[0]
    print('The daily period (1) was chosen for work \n')
    
elif input_type == '2':                                                        
    daily_time_step   = False                                                  
    monthly_time_step = True 
    long_time_step    = False
    ts = time_array[1]
    print('The montly period (2) was chosen for work \n')    
    
elif input_type == '3':                                                        
    daily_time_step   = False                                                  
    monthly_time_step = False    
    long_time_step    = True  
    ts = time_array[2]
    print('The user period (3) was chosen for work \n')   
    
else:
    print ('Error: Incorrect actual period!')
    sys.exit()                                                                          
        
                 
#------------------------------------------------------------------------------
# Select model version of GLEAM data: 1 ---> GLEAM v3.5a; 
#                                     2 ---> GLEAM v3.5b;
#                                     3 ---> GLEAM both versions together
#------------------------------------------------------------------------------
while True:
    #input_version = input('Choose the version of GLEAM data: ' +
    #                      'v3.5_a - A; v3.5_b - B; both - BT \n\n') 

    input_version = f_GLEAM_data    
    if input_version == 'A':                                                    # Use only version 3.5_a                                                          
        lversion_a  = True                                                          
        lversion_b  = False     
        lversion_bt = False        
        print('The GLEAM v3.5_a was chosen: \n')    
        break
        
    elif input_version == 'B':                                                 # Use only version 3.5_b
        lversion_a  = False                                                          
        lversion_b  = True     
        lversion_bt = False        
        print('The GLEAM v3.5_b was chosen: \n')
        break
        
    elif input_version == 'BT':                                                # Use both version 3.5a and 3.5b
        lversion_a  = False                                                          
        lversion_b  = False     
        lversion_bt = True 
        print('The GLEAM v3.5_a and v3.5_b were chosen: \n')
        break
        
    else:
        print ('Error: Incorrect version of GLEAM data \n')
        sys.exit()

#--------------------------------------------------------------------------
# Select domain for research: 1 - Park;
#                             2 - Linden;
#                             3 - Lindenberg;
#--------------------------------------------------------------------------
    
while True:            
    #input_region = input('Choose region: Park - P; Linden - L; ' +
    #                     'Lindenberg - Li \n\n')
    input_region = f_region 
    if input_region == 'P':
        # folder with data
        sssf_region = 'PARC/'
        # filename part
        fn_region   = 'parc'
        print('The Park region was chosen: \n')
        break
        
    elif input_region == 'L':
        # folder with data
        sssf_region = 'LINDEN/'
        # filename part
        fn_region   = 'linden'
        print('The Linden region was chosen: \n')
        break
    
    elif input_region == 'Li':
        # folder with data
        sssf_region = 'LINDENBERG/'
        # filename part
        fn_region   = 'lindenberg'
        print('The Lindenberg region was chosen: \n')
        break    

    else:
        print ('Error: Incorrect format of region')


input_station = f_station
print ('The ' + input_station + ' was chosen \n')

#------------------------------------------------------------------------------
# Get initial COSMO data
#------------------------------------------------------------------------------

parc01_ctr    = csm_data.cosmo_data(mf_com, sf_parc01_ctr    , fn_cosmo, clm_name)
parc_v35      = csm_data.cosmo_data(mf_com, sf_parc_v35      , fn_cosmo, clm_name)
parc_v45      = csm_data.cosmo_data(mf_com, sf_parc_v45      , fn_cosmo, clm_name)
parc_v45_evap = csm_data.cosmo_data(mf_com, sf_parc_v45_evap , fn_cosmo, clm_name)

#------------------------------------------------------------------------------
# Get initial IN-CITY data based on FLUXNET and EURONET data
#------------------------------------------------------------------------------

df_fluxnet, station_name_plot = flnt.fluxnet_data(mf_com, sf_fluxnet, input_mode,
                                                  mylist, input_station)    
    
df_euronet = flnt.euronet_data(mf_com, sf_euronet, input_station)
        
#------------------------------------------------------------------------------
# Get initial REANALYSIS data
#------------------------------------------------------------------------------

if ldaily == daily_time_step:    
    print('The minimum timestep for GLEAM, E-OBS and HYRAS data is daily \n')
else:
    print('Are using EOBS data: \n')
    df_t2m_eobs = radata.eobs_data(mf_com, sf_eobs, fn_region)
        
    print('Are using HYRAS data: \n')
    df_t2m_hyras = radata.hyras_data(mf_com, sf_hyras, parameters, fn_region)
    
    print('Are using GLEAM data: \n') 
    df_gleam = radata.gleam_data(mf_com, sf_gleam, fn_region, 
                                 lversion_a, lversion_b, lversion_bt)        


#------------------------------------------------------------------------------
# Section: Get time periods
#------------------------------------------------------------------------------


if ldaily == daily_time_step:                                                            # daily
    y_w_1 = pd.date_range(start = '2005-06-11', end = '2005-06-12', freq = 'D')                    
    y_w_2 = pd.date_range(start = '2005-06-12', end = '2005-06-13', freq = 'D') 
else:
    if lperiod == monthly_time_step:                                                     # monthly 
        y_w_1 = pd.date_range(start = '2005-01-01', end = '2006-02-01', freq = 'MS')              
        y_w_2 = pd.date_range(start = '2005-01-01', end = '2006-03-01', freq = 'M')                  
    elif lperiod != monthly_time_step and llperiod == long_time_step:                    # user time period
        y_w_1 = pd.to_datetime(['2010-01-01','2011-01-01', '2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01'])
        y_w_2 = pd.to_datetime(['2010-12-31','2011-12-31', '2012-12-31', '2013-12-31', '2014-12-31', '2015-12-31'])                                


#------------------------------------------------------------------------------
# Section: Work with data and data visualization
#------------------------------------------------------------------------------

# Ged monthly date for time periods and plot maps
for  tr in range(len(y_w_1)):   
    #--------------------------------------------------------------------------
    # Create time period with hourly timesteps
    #-------------------------------------------------------------------------- 
    h_period = pd.date_range(y_w_1[tr], y_w_2[tr], freq = 'H')   
    #--------------------------------------------------------------------------
    # Create time period with dayly timesteps
    #--------------------------------------------------------------------------
    d_period = pd.date_range(y_w_1[tr], y_w_2[tr], freq = 'D')   
    
    #--------------------------------------------------------------------------
    # Subsection: Create data for plots
    #--------------------------------------------------------------------------
    
    # COSMO data   
    parc01_l        = csm_data.get_timeseries(clm_name, parc01_ctr   , h_period, ts)  # PARC01_ctr --> original COSMO     
    parc_v35_l      = csm_data.get_timeseries(clm_name, parc_v35     , h_period, ts)  # parc_v35 --> main experiment    
    parc_v45_l      = csm_data.get_timeseries(clm_name, parc_v45     , h_period, ts)  # parc_v45 --> main experiment           
    parc_v45e_l = csm_data.get_timeseries(clm_name, parc_v45_evap, h_period, ts)  # parc_v45_evap --> previous version parc_v45  
    
    #FLUXNET data
    t_2m_mds  = df_fluxnet['T2m'][h_period].resample(ts).mean()  
    ts_mds_1  = df_fluxnet['Ts'][h_period].resample(ts).mean() 
    le_mds    = df_fluxnet['LE'][h_period].resample(ts).mean() 
    le_corr   = df_fluxnet['LE_corr'][h_period].resample(ts).mean() 
    rh_mds    = df_fluxnet['RH'][h_period].resample(ts).mean() 
    vpd_mds   = df_fluxnet['VPD'][h_period].resample(ts).mean() 
    pa_mds    = df_fluxnet['Pa'][h_period].resample(ts).mean()  * 10.0
    qv_s_f    = df_fluxnet['QV_S'][h_period].resample(ts).mean() * 0.0            # temporal --> need to fix it    
    
    #EURONET data
    t_2m_euro   = df_euronet['TA'][h_period].resample(ts).mean()
    t_s_euro    = df_euronet['TS'][h_period].resample(ts).mean()
    netrad_euro = df_euronet['NETRAD'][h_period].resample(ts).mean()
    rh_euro     = df_euronet['RH'][h_period].resample(ts).mean()
    pa_euro     = df_euronet['PA'][h_period].resample(ts).mean() * 10
    h_euro      = df_euronet['H'][h_period].resample(ts).mean()
    le_euro     = df_euronet['LE'][h_period].resample(ts).mean()
    g_euro      = df_euronet['G'][h_period].resample(ts).mean()
    
    
    if ldaily == daily_time_step:
        print('Cannot use a E-OBS  data, because of timestep: no hourly data: \n')
        print('Cannot use a HYRAS data, because of timestep: no hourly data: \n')
        print('Cannot use a GLEAM data, because of timestep: no hourly data: \n')    
    else:
        #HYRAS data
        t2m_hyras = df_t2m_hyras['T_2M'][d_period].resample(ts).mean()        

        #E-OBS data
        t2m_eobs  = df_t2m_eobs['parc'][d_period].resample(ts).mean()       
        
        
        s_zero = pd.Series(np.nan, index = df_gleam.index)
        
        #GLEAM data v3.5a
        try:
            Ep_gleam_a = df_gleam['Ep_a'][d_period].resample(ts).sum()
            #Ep_gleam_a = df_gleam['Ep_a'][d_period]
            Et_gleam_a = df_gleam['Et_a'][d_period].resample(ts).mean()
        except KeyError as error:
            print ( 'Are using GLEAM v3.5b --> not GLEAM v3.5a \n', error )            
            Ep_gleam_a = s_zero[d_period].resample(ts).mean()
            Et_gleam_a = s_zero[d_period].resample(ts).mean()
            
        #GLEAM data v3.5b 
        try:
            Ep_gleam_b = df_gleam['Ep_b'][d_period].resample(ts).sum() 
            #Ep_gleam_b = df_gleam['Ep_b'][d_period]
            Et_gleam_b = df_gleam['Et_b'][d_period].resample(ts).mean()
        except KeyError as error:
            print ( 'Are using GLEAM v3.5a --> not GLEAM v3.5b \n', error )
            Ep_gleam_b = s_zero[d_period].resample(ts).mean()
            Et_gleam_b = s_zero[d_period].resample(ts).mean()           
       
        print('\n')
    

            
    #--------------------------------------------------------------------------
    # Subsection: Data vizualization - Plots for all parameters   
    #--------------------------------------------------------------------------
    
    # Additional information for plot title: General            
    time_int_1 = str(y_w_1[tr])[0:4] + str(y_w_1[tr])[5:7]   + str(y_w_1[tr])[8:10]
    time_int_2 = str(y_w_2[tr])[0:4] + str(y_w_2[tr])[5:7]   + str(y_w_2[tr])[8:10]
    date_ind = 'Time step: ' + str(y_w_1[tr])[0:10] + ' to ' + str(y_w_2[tr])[0:10]           
    name_3   = 'Hours'                                                                       # x - label   
    l_p      = 'upper left'
    nst      = station_name_plot

    for k in range(len(plot_name)):             
        if k == 0:
            print (plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            
            #Plot data AEVAP
            # -----------------------------------------------------------------
            fig   = plt.figure(figsize = (14,10))
            ax    = fig.add_subplot(111)
            try:
                if ldaily == daily_time_step:
                    aevap_plot = vis.plot_4d(ax, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 
                                                 name_1[k], name_2[k], name_3, 
                                                 date_ind, nst, l_p,
                                                 y_min_d[k], y_max_d[k], y_step_d[k],
                                                 y_w_1[tr], y_w_2[tr])
                       
                else:
                    if lperiod == monthly_time_step:
                        aevap_plot = vis.plot_5(ax, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],    Ep_gleam_a,    Ep_gleam_b, 
                                                   'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 'Gleam_v3.5a', 'Gleam_v3.5b',
                                                    name_1[k], name_2[k], date_ind, nst, l_p,
                                                    y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr]) 
                                    
                    elif lperiod != monthly_time_step and llperiod == long_time_step:    
                        aevap_plot = vis.plot_6(ax, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],    Ep_gleam_a,    Ep_gleam_b, 
                                                   'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 'Gleam_v3.5a', 'Gleam_v3.5b',
                                                    name_1[k], name_2[k], date_ind, nst, l_p, 
                                                    y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr]) 
                        
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig)
                plt.gcf().clear()  
        
            except NameError as error:
                print('Exception ' + clm_name[k] + ' ', error)             
            # End plot data AEVAP
            #--------------------------------------------------------------------------            
            
            continue
        
        elif k == 1:
            print (plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data ALHFL_BS
            # -------------------------------------------------------------------------
            fig1  = plt.figure(figsize = (14,10))
            ax1   = fig1.add_subplot(111)
          
            try:
                if ldaily == daily_time_step:
                    alhfl_bs_plot = vis.plot_4d(ax1, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                    'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                     name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                     y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                     
                  
                else:
                    if lperiod == monthly_time_step:
                        alhfl_bs_plot = vis.plot_4(ax1, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                       'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                        name_1[k], name_2[k], date_ind, nst, l_p, 
                                                        y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])
                                       
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        alhfl_bs_plot = vis.plot_4(ax1, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                       'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                          
                                                        name_1[k], name_2[k], date_ind, nst, l_p,
                                                        y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 

                plt.close(fig1)        
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
            
            # End plot data ALHFL-BS
            #--------------------------------------------------------------------------            
            continue            
                      
        
        elif k == 2:
            print (plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data ALHFL_PL
            # -------------------------------------------------------------------------
            fig2  = plt.figure(figsize = (14,10))
            ax2   = fig2.add_subplot(111)
          
            try:
                if ldaily == daily_time_step:
                    alhfl_pl_plot = vis.plot_4d(ax2, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                    'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                     name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                     y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                     
                  
                else:
                    if lperiod == monthly_time_step:
                        alhfl_pl_plot = vis.plot_4(ax2, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                       'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                        name_1[k], name_2[k], date_ind, nst, l_p, 
                                                        y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])
                                       
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        alhfl_pl_plot = vis.plot_4(ax2, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                       'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                          
                                                        name_1[k], name_2[k], date_ind, nst, l_p,
                                                        y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 

                plt.close(fig2)        
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
            
            # End plot data ALHFL-PL
            #--------------------------------------------------------------------------
                continue
        
        
        elif k == 3:
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            
            # Plot data ALHFL_S
            # -----------------------------------------------------------------
            fig3  = plt.figure(figsize = (14,10))
            ax3   = fig3.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                    alhfl_s_plot = vis.plot_6d(ax3, parc01_l[k], parc_v35_l[k], parc_v45_l[k],  parc_v45e_l[k],    le_mds,   le_euro,
                                                   'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',    'Cosmo_v4.5', 'FLUXNET', 'EURONET',
                                                    name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                    y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        alhfl_s_plot = vis.plot_6(ax3, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],    le_mds,   le_euro,
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',   'Cosmo_v4.5', 'FLUXNET', 'EURONET',                                      
                                                       name_1[k], name_2[k], date_ind, nst, l_p, 
                                                       y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        alhfl_s_plot = vis.plot_6(ax3, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],    le_mds,   le_euro,
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',   'Cosmo_v4.5', 'FLUXNET', 'EURONET',                                           
                                                       name_1[k], name_2[k], date_ind, nst, l_p,
                                                       y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png',format = 'png', dpi = 300) 
                
                plt.close(fig3)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
            
            # End plot data ALHFL
            #--------------------------------------------------------------------------            
            
            
            # Plot data ALHFL comparison
            # -----------------------------------------------------------------
            fig4  = plt.figure(figsize = (14,10))
            ax4   = fig4.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                    alhfl_comp = vis.plot_4d(ax4, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                 'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 
                                                  name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                  y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        alhfl_comp = vis.plot_4(ax4, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                    'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                       
                                                     name_1[k], name_2[k], date_ind, nst, l_p, 
                                                     y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        alhfl_comp = vis.plot_4(ax4, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                    'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                           
                                                     name_1[k], name_2[k], date_ind, nst, l_p,
                                                     y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + 'com_' + time_int_1 + '_' +
                            time_int_2 + '.png',format = 'png', dpi = 300) 
                
                plt.close(fig4)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + 'com', error) 
            
            # End plot data ALHFL
            #--------------------------------------------------------------------------            
                                  
            continue            
        
        
        
        elif k == 4:
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            
            # Plot data ASHFL_S 
            # -----------------------------------------------------------------
            fig5  = plt.figure(figsize = (14,10))
            ax5   = fig5.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                    alhfl_s_plot = vis.plot_4d(ax5, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                   'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 
                                                    name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                    y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        alhfl_s_plot = vis.plot_4(ax5, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                      
                                                       name_1[k], name_2[k], date_ind, nst, l_p, 
                                                       y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        alhfl_s_plot = vis.plot_4(ax5, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                           
                                                       name_1[k], name_2[k], date_ind, nst, l_p,
                                                       y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig5)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
            
            # End plot data ASHFL
            #--------------------------------------------------------------------------              
        
            continue
        
        elif k == 5:
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            
            # Plot data AZTRALEAV 
            # -----------------------------------------------------------------        
            fig6  = plt.figure(figsize = (14,10))
            ax6   = fig6.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                   ztraleav_plot = vis.plot_4d(ax6, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                   'Cosmo_orig',  'Cosmo_v3.5', 'Cosmo_v4.5',   'Cosmo_v4.5e', 
                                                     name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                     y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        ztraleav_plot = vis.plot_4(ax6, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                       'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                      
                                                         name_1[k], name_2[k], date_ind, nst, l_p, 
                                                         y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        ztraleav_plot = vis.plot_4(ax6, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                       'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                            
                                                         name_1[k], name_2[k], date_ind, nst, l_p,
                                                         y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig6)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
        
            # End plot data AZTRALEAV
            #--------------------------------------------------------------------------              
        
            continue        
        
        elif k == 6:
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            
            # Plot data AZTRANG 
            # -----------------------------------------------------------------        
      
            fig7  = plt.figure(figsize = (14,10))
            ax7   = fig7.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                    ztrang_plot = vis.plot_4d(ax7, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 
                                                    name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                    y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        ztrang_plot = vis.plot_4(ax7, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                     'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                      
                                                       name_1[k], name_2[k], date_ind, nst, l_p, 
                                                       y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        ztrang_plot = vis.plot_4(ax7, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                     'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                            
                                                       name_1[k], name_2[k], date_ind, nst, l_p,
                                                       y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig7)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error)         
            # End plot data AZTRANG
            #--------------------------------------------------------------------------              
        
            continue        
        
        
        elif k == 7:
            # Plot data ZTRANGS
            # -----------------------------------------------------------------
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            fig8  = plt.figure(figsize = (14,10))
            ax8   = fig8.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                    ztrangs_plot = vis.plot_4d(ax8, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                   'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 
                                                     name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                     y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        ztrangs_plot = vis.plot_4(ax8, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                      
                                                        name_1[k], name_2[k], date_ind, nst, l_p, 
                                                        y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        ztrangs_plot = vis.plot_4(ax8, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                           
                                                        name_1[k], name_2[k], date_ind, nst, l_p,
                                                        y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig8)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error)               
            # Plot data ZTRANGS 
            # -----------------------------------------------------------------        
        
      
        
            continue         

        
        elif k == 8:
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            
            # Plot data AZVERBO 
            # -----------------------------------------------------------------        
            fig9  = plt.figure(figsize = (14,10))
            ax9   = fig9.add_subplot(111)
                  
            try:
                if ldaily == daily_time_step:
                    zverbo_plot = vis.plot_4d(ax9, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e', 
                                                    name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                    y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                       
                                           
                else:
                    if lperiod == monthly_time_step:
                        zverbo_plot = vis.plot_4(ax9, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                     'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                      
                                                       name_1[k], name_2[k], date_ind, nst, l_p, 
                                                       y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])    
        
                                   
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        zverbo_plot = vis.plot_6(ax9, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], Et_gleam_a, Et_gleam_b,                                    
                                                     'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',  'GLEAM a',  'GLEAM b',                                          
                                                       name_1[k], name_2[k], date_ind, nst, l_p,
                                                       y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                          
                  
                        
                        
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig9)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error)           
            # End plot data ZVERBO
            #--------------------------------------------------------------------------              
        
            continue              
        
        elif k == 9:
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)

            # Plot data QV_2M
            # -------------------------------------------------------------------------
            fig10  = plt.figure(figsize = (14,10))
            ax10   = fig10.add_subplot(111)             
            
            try:
                if ldaily == daily_time_step:
                    qv_plot = vis.plot_4d(ax10, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                               'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                           
                                                  name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                  y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                    
                else:
                    if lperiod == monthly_time_step:
                        qv_plot = vis.plot_4(ax10, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                              
                                                     name_1[k], name_2[k], date_ind, nst, l_p,
                                                     y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])                                         
                    
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        qv_plot = vis.plot_4(ax10, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k],
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                         
                                                     name_1[k], name_2[k], date_ind, nst, l_p,
                                                     y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                       
                
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png',format = 'png', dpi = 300) 
                
                plt.close(fig10)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
            
            # End plot data QV_2M
            #--------------------------------------------------------------------------
            continue        
        
        elif k == 10:

            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data QV_S
            # -------------------------------------------------------------------------
            fig11  = plt.figure(figsize = (14,10))
            ax11   = fig11.add_subplot(111)               
            
            try:
                if ldaily == daily_time_step:
                    qv_s_plot = vis.plot_4d(ax11, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                 'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                 name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                 y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                     
                else:
                    if lperiod == monthly_time_step:
                        qv_s_plot = vis.plot_4(ax11, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                    'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                    name_1[k], name_2[k], date_ind, nst, l_p,
                                                    y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])      
                                            
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        qv_s_plot = vis.plot_4(ax11, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                    'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                    name_1[k], name_2[k], date_ind, nst, l_p,
                                                    y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])  
                          
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig11)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
        
            # End plot data QV_S
            #--------------------------------------------------------------------------
            continue        
        

        elif k == 11:
      
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data RELHUM
            # -------------------------------------------------------------------------    
            fig12  = plt.figure(figsize = (14,10))
            ax12   = fig12.add_subplot(111)                                                                       
            
            try:
                if ldaily == daily_time_step:
                    relhum_plot = vis.plot_4d(ax12, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                   'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                   name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                   y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                       
                else:
                    if lperiod == monthly_time_step:                                  
                        relhum_plot = vis.plot_4(ax12, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                      name_1[k], name_2[k], date_ind, nst, l_p, 
                                                      y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])                                              
                        
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        relhum_plot = vis.plot_4(ax12, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                      'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                      name_1[k], name_2[k], date_ind, nst, l_p,
                                                      y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                
                
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig12)    
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
                
            # End plot data RELHUM
            #--------------------------------------------------------------------------        
            continue



        elif k == 12:
      
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data RSTOM
            # -------------------------------------------------------------------------    
            fig13  = plt.figure(figsize = (14,10))
            ax13   = fig13.add_subplot(111)                                                                       
            
                          
            
            try:
                if ldaily == daily_time_step:
                    rstom_plot = vis.plot_4d(ax13, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                   name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                   y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                       
                else:
                    if lperiod == monthly_time_step:                                  
                        rstom_plot = vis.plot_4(ax13, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                     'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                      name_1[k], name_2[k], date_ind, nst, l_p, 
                                                      y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])                                              
                        
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        rstom_plot = vis.plot_4(ax13, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                     'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                      name_1[k], name_2[k], date_ind, nst, l_p,
                                                      y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                
                
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png', format = 'png', dpi = 300) 
                
                plt.close(fig13)    
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
                
            # End plot data RELHUM
            #--------------------------------------------------------------------------        
            continue



        elif k == 13:
    
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data T2M
            # -------------------------------------------------------------------------    
            fig14  = plt.figure(figsize = (14,10))
            ax14   = fig14.add_subplot(111)             
            
            try:
                if ldaily == daily_time_step:
                    t2m_plot = vis.plot_4d(ax14, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',     
                                                 name_1[k],  name_2[k], name_3, date_ind, nst, l_p,
                                                 y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                
                else:
                    if lperiod == monthly_time_step:      
                        t2m_plot = vis.plot_6(ax14, parc01_l[k],  parc_v35_l[k], parc_v45_l[k],  parc_v45e_l[k], t2m_hyras, t2m_eobs, 
                                                   'Cosmo_orig',   'Cosmo_v3.5',  'Cosmo_v4.5',   'Cosmo_v4.5e',   'HYRAS',   'EOBS',  
                                                    name_1[k], name_2[k], date_ind, nst, l_p, 
                                                    y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])   
                                            
                    elif lperiod != monthly_time_step and llperiod == long_time_step:      
                        t2m_plot = vis.plot_6(ax14, parc01_l[k],  parc_v35_l[k], parc_v45_l[k],  parc_v45e_l[k], t2m_hyras, t2m_eobs, 
                                                   'Cosmo_orig',   'Cosmo_v3.5',  'Cosmo_v4.5',   'Cosmo_v4.5e',   'HYRAS',   'EOBS',
                                                    name_1[k], name_2[k], date_ind, nst, l_p,
                                                    y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])           
                
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png',format = 'png', dpi = 300) 
                
                plt.close(fig14)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
                
            # End plot data T2m
            #--------------------------------------------------------------------------
            continue
    
        elif k == 14:
            
            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data TS
            # -------------------------------------------------------------------------    
            fig15  = plt.figure(figsize = (14,10))
            ax15   = fig15.add_subplot(111)      
            
            try:
                if ldaily == daily_time_step:
                    ts_plot = vis.plot_4d(ax15, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                               'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',  
                                                name_1[k],  name_2[k], name_3, date_ind, nst, l_p,
                                                y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])                                   
                else:
                    if lperiod == monthly_time_step:                                   
                        ts_plot = vis.plot_4(ax15, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',  
                                                   name_1[k], name_2[k], date_ind, nst, l_p, 
                                                   y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])                                      
                                              
                    elif lperiod != monthly_time_step and llperiod == long_time_step:      
                        ts_plot = vis.plot_4(ax15, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                     
                                                   name_1[k], name_2[k], date_ind, nst, l_p,
                                                   y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])           
              
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png',format = 'png', dpi = 300) 
                
                plt.close(fig15)
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
                
            # End plot data TS
            #--------------------------------------------------------------------------                    
            continue
        
        elif k == 15:       

            print(plot_name[k] + ' period: ' + time_int_1 + ' to ' + time_int_2)
            # Plot data PS
            # -------------------------------------------------------------------------
            fig16  = plt.figure(figsize = (14,10))
            ax16   = fig16.add_subplot(111)                        
            try:
                if ldaily == daily_time_step:
                    ps_plot = vis.plot_4d(ax16, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                               'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                  
                                                name_1[k], name_2[k], name_3, date_ind, nst, l_p,
                                                y_min_d[k], y_max_d[k], y_step_d[k], y_w_1[tr], y_w_2[tr])         
                else:
                    if lperiod == monthly_time_step:
                        ps_plot = vis.plot_4(ax16, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',
                                                   name_1[k], name_2[k], date_ind, nst, l_p,
                                                   y_min_m[k], y_max_m[k], y_step_m[k], y_w_1[tr], y_w_2[tr])
                                       
                    elif lperiod != monthly_time_step and llperiod == long_time_step:
                        ps_plot = vis.plot_4(ax16, parc01_l[k], parc_v35_l[k], parc_v45_l[k], parc_v45e_l[k], 
                                                  'Cosmo_orig',  'Cosmo_v3.5',  'Cosmo_v4.5',  'Cosmo_v4.5e',                                       
                                                   name_1[k], name_2[k], date_ind, nst, l_p,
                                                   y_min_u[k], y_max_u[k], y_step_u[k], y_w_1[tr], y_w_2[tr])                                         
                               
                plt.savefig(result_path[k] + clm_name[k] + '_' + time_int_1 + '_' +
                            time_int_2 + '.png',format = 'png', dpi = 300) 

                plt.close(fig16)        
                plt.gcf().clear()  
        
            except NameError as error:
                print ('Exception ' + clm_name[k] + ' ', error) 
            
            # End plot data PS
            #--------------------------------------------------------------------------           
       
            continue
             
  
        else:
            print('No data from list')            






            
     
 
    
 
    
 

   

   


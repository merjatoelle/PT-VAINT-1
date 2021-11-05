# -*- coding: utf-8 -*-
"""
The stat_module is the main programm for statistical analysis of COSMO data
There are several options for statistical analysis, moreover there are options
for data visualization of annual, diurnal, mothly and hourly data. There is 
option for heat and cold wave visualization and option for weekly verification 
plots. 
   

The progam contains several personal modules:
    fluxnet_data    ---> personal module for work with IN-SITU data (FLUXNET, EURONET)
    cosmo_data      ---> personal module for work with MODEL data   (COSMO)
    reanalysis_data ---> personal module for work with HYRAS, E-OBS, GLEAM data
    insitu_data     ---> personal module for work with Linden and Lindenberg data
    stat_functions  ---> personal module for work with statistical analysis
    vis_module      ---> personal module for data visualization
                                   
The progam contains several subroutines for:
    
    Data visualization:
        mode = 1 ---> Get annual cycle based on daily (climatic) values
        mode = 2 ---> Get values for June based on daily values
        mode = 3 ---> Get diurnal cycle based on hourly values        
        mode = 4 ---> Get weekly values based on hourly data (verification plots)
        mode = 5 ---> Get heat and cold waves
        mode = 6 ---> Get mean values for one week based on average (5 years) 
                      hourly data
    
    Statistical analysis:
        mode = 7 ---> Get statistical analysis: a - compare to in-situ data
                                                b - COSMO data    
        mode = 8 ---> Get statistical analysis based on field data
        
    Taylor diagram
        mode = 9 ---> Get plots with Taylors diagrams 


                                                
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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import personal libraries
import fluxnet_data      as flnt                                                             
import cosmo_data        as csm_data                                           
import reanalysis_data   as radata                                             
import vis_module        as vsp                                                 
import insitu_data       as isd
import stat_functions    as stf                                                



#------------------------------------------------------------------------------
# Main programm
#------------------------------------------------------------------------------

# Choose your option for work (Possible options: 1 - Get average monhtly values (climatic))
#                                                2 - Get avarage daily values   (climatic)  for June
#                                                3 - Get diurnal values         (climatic)  
#                                                4 - Get verification plots 
#                                                5 - Get heat waves  
#                                                6 - Statistic analysis  
#                                                7 - Get summer values 
#                                                8
#                                                9
#                                               10 

mode = 6                                                                        




# Choose your region for analysis (Possible options: 1 - PARC domain
#                                                    2 - LINDEN domain
#                                                    3 - LINDENBERG domain )

input_region = '1'


while True: 
    if input_region == '1':
        domain    = 'PARC'                                                     # Name of folder for COSMO data
        fn_region = 'parc'                                                     # Name of file for GLEAM data
        station_plot = 'Rollesbroich'
        break
    
    elif input_region == '2':
        domain         = 'LINDEN'
        fn_region      = 'linden'
        station_plot   = 'Linden'
        sf_in_situ     = 'IN-SITU/' + domain + '/'
        fn_in_situ     = 'EC4.csv'
        break
    
    elif input_region == '3':
        domain         = 'LINDENBERG'
        fn_region      = 'lindenberg'
        station_plot   = 'Lindenberg'
        sf_in_situ     = 'IN-SITU/' + domain + '/'
        fn_in_situ     = 'Lindenberg.csv'
        break
    else:
        print('Error: Incorrect format of region')
    
    
#------------------------------------------------------------------------------
# Setting paths for COSMO, EURONET, FLUXNET, GLEAM, HYRAS, E-OBS data
#------------------------------------------------------------------------------
mf_com    = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'                        # Main path for project  
data_exit = mf_com + '/ANALYSIS/PLOTS/' + domain + '/'                         # Main path for project results

sf_cclm_ref  = mf_com + 'COSMO/' + domain + '/CTR/'                            # Path for CCLM_ref  data                
sf_cclm_v35  = mf_com + 'COSMO/' + domain + '/v3.5/'                           # Path for CCLMv3.5  data                
sf_cclm_v45  = mf_com + 'COSMO/' + domain + '/v4.5/'                           # Path for CCLMv4.5  data               
sf_cclm_v45e = mf_com + 'COSMO/' + domain + '/v4.5e/'                          # Path for CCLMv4.5e data    

sf_fluxnet   = mf_com + 'IN-SITU/FLUXNET/'                                     # Path for FLUXNET data    
sf_euronet   = mf_com + 'IN-SITU/EURONET/'                                     # Path for EURONET data
sf_gleam     = mf_com + 'REANALYSIS/GLEAM/'                                    # Path for GLEAM   data
sf_hyras     = mf_com + 'REANALYSIS/HYRAS/'                                    # Path for HYRAS   data
sf_eobs      = mf_com + 'REANALYSIS/EOBS/'                                     # Path for E-OBS   data 

#------------------------------------------------------------------------------
# Setting for COSMO data
#------------------------------------------------------------------------------

                                
# Names of parameters for COSMO data
clm_name = ['AEVAP_S', 'ALHFL_S' , 'ASHFL_S', 'RSTOM'   ,
            'ZVERBO' , 'T_2M'    , 'T_S'    , 'TMAX_2M' ,
            'TMIN_2M', 'ZTRALEAV']

#r'$H_{2}$'

if mode == 3:
    name_2   = ['AEVAP_S, kg m-2', 'ALHFL_S, W m-2'   , 'ASHFL_S, W m-2' , 
                'RSTOM, s m-1'   , 'ZVERBO, mm hour-1', 'T_2M, C' + u"\N{DEGREE SIGN}", 
                'T_S, C' + u"\N{DEGREE SIGN}", 'TMAX_2M, C' + u"\N{DEGREE SIGN}", 'TMIN_2M, C'  + u"\N{DEGREE SIGN}",
                'ZTRALEAV, mm hour-1' ]
elif mode == 4:
    name_2   = ['AEVAP_S, kg m-2', 'ALHFL_S, W m-2'   , 'ASHFL_S, W m-2' , 
                'RSTOM, s m-1'   , 'ZVERBO, mm hour-1', 'T_2M, C' + u"\N{DEGREE SIGN}", 
                'T_S, C' + u"\N{DEGREE SIGN}", 'TMAX_2M, C' + u"\N{DEGREE SIGN}", 'TMIN_2M, C' + u"\N{DEGREE SIGN}",
                'ZTRALEAV, mm hour-1' ]    
    
else:
    name_2   = ['AEVAP_S, kg m \u207b\u00B2'  , 'ALHFL_S, W m \u207b\u00B2'       , 'ASHFL_S, W m \u207b\u00B2'     , 
                'RSTOM, s m \u207b\u00B9'     , 'ZVERBO, mm day \u207b\u00B9'    , 'T_2M, C' + u"\N{DEGREE SIGN}"   , 
                'T_S, C' + u"\N{DEGREE SIGN}", 'TMAX_2M, C' + u"\N{DEGREE SIGN}", 'TMIN_2M, C'  + u"\N{DEGREE SIGN}",
                'ZTRALEAV, mm day \u207b\u00B9']
    
# Name of COSMO data
fn_cosmo = '_ts_mean_1999_2015.csv'

# Input station
input_station = 'RuR'

# Timestep for data (need for pd.resample)
time_step     = '1D'

#------------------------------------------------------------------------------
# Settings for field statistical analysis 
#------------------------------------------------------------------------------

'''
For the first version only the HYRAS option is available

The main dataset with observations, there are several options: refer = 'HYRAS'
                                                                       'EOBS'
                                                                       'GLEAM'

ds_name - is a parameter for statistical analysis (dataset with expeiments)    

options: 'COSMO_ORIG'; 'COSMO_35'; 'COSMO_45'; 'COSMO_45e'


for KGE metric I used: HYRAS data        --> dataset with observations
                       COSMO_ORIG        --> option 1 for comparison
                       COSMO_35, 45, 45e --> options 2,3,4 for comparisons

for DAV metric I used: HYRAS data        --> dataset with observations (obs)
                       COSMO_ORIG        --> dataset for comparison    (lr)
                       COSMO_35, 45, 45e --> options for analysis      (hr)

Because of that the parameter ds_name has 4 options, however in DAV metric 
this parameter will be equal 0 because we compare COSMO_ORIG wirh COSMO_ORIG



PS. Now the T_2M parameter are using for comparison, if you want to use different
you have to change it it stat_analysis file, moreover in DAV_metric you have to
change pdf limits

PS2. You have to change Tailor diagram parameters by your hand
'''

refer = 'HYRAS' #GLEAM

if refer == 'HYRAS':
    #HYRAS
    sf_statistic = 'ANALYSIS/FIELD_STAT/'
    # Parameter list for field analysis (mode 8) HYRAS
    par_list = ['T_2M', 'T_MAX', 'T_MIN', 'T_S']
else:
    #GLEAM
    sf_statistic = 'ANALYSIS/FIELD_STAT_GLEAM/'
    
    # Parameter list for field analysis (mode 8) GLEAM
    par_list = ['AEVAP_S', 'ZVERBO']
    
   
# Special parameter for GLEAM dataset
vrs_GLEAM = 'v3.5b'

ds_name = 'COSMO_45e'
# Path for statistic results and Tailor diagramm
path_exit = mf_com + sf_statistic      

# Paths for subfolders for KGE and RMSD data
sf_field_stat = mf_com + sf_statistic + domain + '/'                           # The subfolder for refer data (observation)
      
#------------------------------------------------------------------------------
# Additional settings (timestep and limits for y-axis for plots)
#------------------------------------------------------------------------------

# Define the scales limits: y_min - lower limit, y_max - upper limit, y_step - step
if mode == 1:
    #            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,  ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
    y_min  = [   0.0 ,      0.0,    -50.0,       0.0,     0.0 ,    0.0,    0.0,    0.0,     0.0,    0.0 ]
    y_max  = [   4.01,    110.1,     75.1,   20000.1,     4.01,   25.1,   25.1,   25.1,    25.1,    3.01]
    y_step = [   0.5 ,     10.0,     25.0,    2000.0,     0.5 ,    5.0,    5.0,    5.0,     5.0,    0.5 ]  

elif mode == 2:
    #            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
    y_min  = [   0.0,      0.0,    -50.0,       0.0,     0.0 ,    5.0,    5.0,    5.0,     5.0,     0.0 ]
    y_max  = [  4.01,    150.1,     75.1,   10000.1,     6.1 ,   30.1,   30.1,   30.1,    30.1,     4.01]
    y_step = [   0.5,     10.0,     25.0,    1000.0,     1.0 ,    5.0,    5.0,    5.0,     5.0,     0.5 ]  

elif mode == 3:
    #            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
    y_min  = [   0.0,      0.0,    -50.0,       0.0,     0.0 ,   10.0,   10.0,    0.0,     0.0,     0.0]
    y_max  = [  0.51,    250.1,    200.1,   10000.1,     8.1 ,   30.1,   30.1,   25.1,    25.1,     6.0]
    y_step = [   0.1,     25.0,     25.0,    1000.0,     1.0 ,    2.0,    2.0,    5.0,     5.0,     1.0]  

elif mode == 10:
    #            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
    y_min  = [   0.0,      0.0,    -50.0,       0.0,     0.5 ,   10.0,   10.0,     10.0,     0.0,     0.0]
    y_max  = [  5.01,    150.1,    150.1,    4000.1,    7.51 ,   30.1,   30.1,     35.1,    25.1,     5.1] #2250
    y_step = [   0.5,     25.0,     25.0,     500.0,     1.0 ,    2.0,    2.0,      5.0,     5.0,     0.5] #250 
else:
    #            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
    y_min  = [   0.0,      0.0,   -100.0,       0.0,     0.0 ,   10.0,   10.0,   10.0,    10.0,     0.0]
    y_max  = [  0.51,    325.1,    350.1,   10000.1,    15.1 ,   40.1,   40.1,   40.1,    40.1,     9.1]
    y_step = [   0.1,     25.0,     50.0,    1000.0,     1.0 ,    5.0,    5.0,    5.0,     5.0,     1.0]  

#------------------------------------------------------------------------------
# Get initial data
#------------------------------------------------------------------------------
df_cclm_ref  = csm_data.cosmo_data(sf_cclm_ref , fn_cosmo, clm_name)           # Get COSMO_ref  data
df_cclm_v35  = csm_data.cosmo_data(sf_cclm_v35 , fn_cosmo, clm_name)           # Get COSMOv3.5  data
df_cclm_v45  = csm_data.cosmo_data(sf_cclm_v45 , fn_cosmo, clm_name)           # Get COSMOv4.5  data
df_cclm_v45e = csm_data.cosmo_data(sf_cclm_v45e, fn_cosmo, clm_name)           # Get COSMOv4.5e data

# The FLUXNET and EURONET has a hourly timestep
df_fluxnet, station_name_plot = flnt.fluxnet_data(sf_fluxnet, input_station)   # get FLUXNET data
df_euronet                    = flnt.euronet_data(sf_euronet, input_station)   # get EORONET data        
        
# The GLEAM, E-OBS and HYRAS datasets has a daily timestep
df_eobs          = radata.eobs_data(sf_eobs, fn_region)                        # get E-OBS data
df_hyras         = radata.hyras_data(sf_hyras, fn_region)                      # get HYRAS data
df_v35a, df_v35b = radata.gleam_data(sf_gleam, fn_region)                      # get GLEAM data


#------------------------------------------------------------------------------
# Get Lindenberg and Linden data
#------------------------------------------------------------------------------
if input_region == '1':
    print ('We are using data from FLUXNET for PARC domain')    
else:
    print ('We are using data from Linden or Lindenberg')
    df_in_situ = isd.get_data(mf_com, sf_in_situ, fn_in_situ)
    df_in_situ = df_in_situ[~df_in_situ.index.duplicated()]


#------------------------------------------------------------------------------
# Main part
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Get average monhtly values (climatic)
#------------------------------------------------------------------------------
if mode == 1:
 
    # Create time period
    time_start = pd.to_datetime(['2013-01-01'   ])
    time_stop  = pd.to_datetime(['2013-12-31 23'])
    
    t_start   = 6                                                              # parameter --> from  
    t_stop    = 18                                                             # parameter --> to  
    
    #--------------------------------------------------------------------------
    # Create time periods 
    #-------------------------------------------------------------------------- 
    hourly_period = pd.date_range(time_start[0], time_stop[0], freq = 'H')     # hourly timesteps
    daily_period  = pd.date_range(time_start[0], time_stop[0], freq = 'D')     # dayly timesteps 
        
    # General time period for COSMO, FLUXNET and EURONET data
    res_period   = [x for x in hourly_period if x.hour >= t_start and x.hour <= t_stop]

    # Get COSMO data
    cclm_ref  = csm_data.cosmo_montly_data(df_cclm_ref , clm_name, hourly_period, time_step )
    cclm_v35  = csm_data.cosmo_montly_data(df_cclm_v35 , clm_name, hourly_period, time_step )
    cclm_v45  = csm_data.cosmo_montly_data(df_cclm_v45 , clm_name, hourly_period, time_step )
    cclm_v45e = csm_data.cosmo_montly_data(df_cclm_v45e, clm_name, hourly_period, time_step )    

    # Get FLUXNET and EURONET data     
    if input_region == '1':                                                    # Parc
        lh = flnt.montly_data(df_fluxnet['LE']      , hourly_period, time_step) 
        sh = flnt.montly_data(df_euronet['H']       , hourly_period, time_step)    
    elif input_region == '2':                                                  # Linden
        lh = flnt.montly_data(df_in_situ['LatHeat'] , hourly_period, time_step)
        sh = flnt.montly_data(df_in_situ['SensHeat'], hourly_period, time_step) 
    else:                                                                      # Lindenberg
        lh = flnt.montly_data(df_in_situ['LHFL_1']  , hourly_period, time_step)
        sh = flnt.montly_data(df_in_situ['SHFL_1']  , hourly_period, time_step)    
    
    # Get Hyras data
    t2m  = flnt.montly_data(df_hyras['T_2M'] , daily_period, time_step)
    tmax = flnt.montly_data(df_hyras['T_MAX'], daily_period, time_step)
    tmin = flnt.montly_data(df_hyras['T_MIN'], daily_period, time_step)
    ts   = flnt.montly_data(df_hyras['T_S']  , daily_period, time_step)
    
    # Get GLEAM data v3.5a 
    ep_v35a = flnt.montly_data(df_v35a['Ep'], daily_period, time_step)                
    et_v35a = flnt.montly_data(df_v35a['Et'], daily_period, time_step)             

    # Get GLEAM data v3.5b
    ep_v35b = flnt.montly_data(df_v35b['Ep'], daily_period, time_step)
    et_v35b = flnt.montly_data(df_v35b['Et'], daily_period, time_step)   
    
    
          
    # Create a new dataframe with GLEAM, FLUXNET and EURONET data
    df_obs = pd.concat([lh, sh, ep_v35a, et_v35a, 
                                ep_v35b, et_v35b,
                                t2m    , tmax, tmin, ts], axis = 1)

    # Rename columnsin dataframe with observations
    df_obs.columns = ['LE', 'H', 'Ep_a', 'Et_a', 
                                 'Ep_b', 'Et_b',
                                 'T_2M', 'TMAX', 'TMIN', 'TS'  ]

    # Plot parc data
    for i in range(len(clm_name)):
        plot = vsp.get_m(cclm_ref   , cclm_v35 , cclm_v45 , cclm_v45e, df_obs ,
                         clm_name[i], name_2[i], data_exit, 
                         y_min[i]   , y_max[i] , y_step[i], input_region)

#------------------------------------------------------------------------------
# Data for one month
#------------------------------------------------------------------------------          
elif mode == 2:                                                                # Get avarage daily values (climatic)
    # Create time period
    time_start = pd.to_datetime(['2010-06-01'   , '2011-06-01'   , '2012-06-01 '  , 
                                 '2013-06-01'   , '2014-06-01'   , '2015-06-01'   ])
    
    time_stop  = pd.to_datetime(['2010-06-30 23', '2011-06-30 23', '2012-06-30 23', 
                                 '2013-06-30 23', '2014-06-30 23', '2015-06-30 23'])  
       
    #--------------------------------------------------------------------------
    # Create time periods 
    #--------------------------------------------------------------------------
    periods_hour = []
    periods_days = [] 
    
    for time_index in range(len(time_start)):
        hourly_period = pd.date_range(time_start[time_index],
                                      time_stop[time_index], freq = 'H')       # hourly timesteps
        
        daily_period  = pd.date_range(time_start[time_index],
                                      time_stop[time_index], freq = 'D')       # dayly timesteps 
        
        periods_hour.append(hourly_period)
        periods_days.append(daily_period)
    
     
    # Get climatic mean values for each day in June for COSMO data
    cclm_ref  = csm_data.cosmo_daily_data(df_cclm_ref , clm_name, periods_hour, time_step) 
    cclm_v35  = csm_data.cosmo_daily_data(df_cclm_v35 , clm_name, periods_hour, time_step) 
    cclm_v45  = csm_data.cosmo_daily_data(df_cclm_v45 , clm_name, periods_hour, time_step) 
    cclm_v45e = csm_data.cosmo_daily_data(df_cclm_v45e, clm_name, periods_hour, time_step) 
 
    # Get Hyras data
    t2m   = flnt.daily_data(df_hyras['T_2M'] , 'HYRAS', time_start, time_stop, time_step)  
    tmax  = flnt.daily_data(df_hyras['T_MAX'], 'HYRAS', time_start, time_stop, time_step)
    tmin  = flnt.daily_data(df_hyras['T_MIN'], 'HYRAS', time_start, time_stop, time_step)
    tsurf = flnt.daily_data(df_hyras['T_S']  , 'HYRAS', time_start, time_stop, time_step)    

    
    # Get GLEAM v3.5a data    
    ep_v35a = flnt.daily_data(df_v35a['Ep'], 'GLEAM', time_start, time_stop, time_step)
    et_v35a = flnt.daily_data(df_v35a['Et'], 'GLEAM', time_start, time_stop, time_step)   
      
    # Get GLEAM v3.5b data    
    ep_v35b = flnt.daily_data(df_v35b['Ep'], 'GLEAM', time_start, time_stop, time_step)
    et_v35b = flnt.daily_data(df_v35b['Et'], 'GLEAM', time_start, time_stop, time_step)
    

    # Get FLUXNET and EURONET data   
    if input_region == '1':                                                    # Parc domain
        lh = flnt.daily_data(df_fluxnet['LE']      , 'FLUX', time_start, time_stop, time_step)
        sh = flnt.daily_data(df_euronet['H']       , 'EURO', time_start, time_stop, time_step)
    elif input_region == '2':                                                  # Linden domain
        lh = flnt.daily_data(df_in_situ['LatHeat'] , 'FLUX', time_start, time_stop, time_step)
        sh = flnt.daily_data(df_in_situ['SensHeat'], 'FLUX', time_start, time_stop, time_step) 
    else:                                                                      # Lindenberg domain
        lh = flnt.daily_data(df_in_situ['LHFL_1']  , 'FLUX', time_start, time_stop, time_step)
        sh = flnt.daily_data(df_in_situ['SHFL_1']  , 'FLUX', time_start, time_stop, time_step)      
    
    # Create a new dataframe with GLEAM, FLUXNET and EURONET data
    df_obs = pd.concat([lh, sh, ep_v35a, et_v35a, 
                                ep_v35b, et_v35b,
                                t2m, tmax, tmin, tsurf], axis = 1)
    
    # Rename columnsin dataframe with observations
    df_obs.columns = ['LE', 'H', 'Ep_a', 'Et_a',
                                 'Ep_b', 'Et_b',
                                 'T_2M', 'TMAX', 'TMIN', 'TS' ]
    
    for i in range(len(clm_name)):
        plot_d = vsp.get_d(cclm_ref   , cclm_v35 , cclm_v45 , cclm_v45e, df_obs,
                           clm_name[i], name_2[i], data_exit,
                           y_min[i]   , y_max[i] , y_step[i], input_region)

#------------------------------------------------------------------------------
# Get diurnal values
#------------------------------------------------------------------------------
elif mode == 3:

    # Create time period
   
    time_start = pd.to_datetime(['2010-06-01'   , '2011-06-01'   , '2012-06-01 '  , 
                                 '2013-06-01'   , '2014-06-01'   , '2015-06-01'   ])
    
    time_stop  = pd.to_datetime(['2010-06-30 23', '2011-06-30 23', '2012-06-30 23', 
                                 '2013-06-30 23', '2014-06-30 23', '2015-06-30 23'])  
       
    #--------------------------------------------------------------------------
    # Create time periods 
    #--------------------------------------------------------------------------
    periods_hour = []
    periods_days = [] 
    
    for time_index in range(len(time_start)):
        hourly_period = pd.date_range(time_start[time_index],
                                      time_stop[time_index], freq = 'H')       # hourly timesteps
        
        daily_period  = pd.date_range(time_start[time_index],
                                      time_stop[time_index], freq = 'D')       # dayly timesteps 
        
        periods_hour.append(hourly_period)
        periods_days.append(daily_period)    

    time_step = '1H'
    # Get COSMO data
    cclm_ref  = csm_data.cosmo_hd(df_cclm_ref , clm_name, periods_hour, time_step) 
    cclm_v35  = csm_data.cosmo_hd(df_cclm_v35 , clm_name, periods_hour, time_step) 
    cclm_v45  = csm_data.cosmo_hd(df_cclm_v45 , clm_name, periods_hour, time_step) 
    cclm_v45e = csm_data.cosmo_hd(df_cclm_v45e, clm_name, periods_hour, time_step) 
    
    
    # Get FLUXNET data
    if input_region == '1':
        # Parc
        lh = flnt.hourly_data(time_start, time_stop, df_fluxnet['LE']  ) 
        sh = flnt.hourly_data(time_start, time_stop, df_euronet['H']   )
    elif input_region == '2':
        # Linden
        lh = flnt.hourly_data(time_start, time_stop, df_in_situ['LatHeat'] )
        sh = flnt.hourly_data(time_start, time_stop, df_in_situ['SensHeat'])        
    else:
        # Lindenberg
        lh = flnt.hourly_data(time_start, time_stop, df_in_situ['LHFL_1'])
        sh = flnt.hourly_data(time_start, time_stop, df_in_situ['SHFL_1'])          
    
    # Create a new dataframe with GLEAM, FLUXNET and EURONET data
    df_obs = pd.concat([lh, sh], axis = 1)
    
    # Rename columnsin dataframe with observations
    df_obs.columns = ['LE', 'H' ]
    

    for i in range(len(clm_name)):
        plot = vsp.get_h(cclm_ref   , cclm_v35 , cclm_v45 , cclm_v45e, df_obs,
                         clm_name[i], name_2[i], data_exit, 
                         y_min[i]   , y_max[i] , y_step[i], input_region     )    
        

#------------------------------------------------------------------------------
# Get weekly values
#------------------------------------------------------------------------------
elif mode == 4:
    #--------------------------------------------------------------------------
    # Get verification plots
    #--------------------------------------------------------------------------
    
    t_1h = pd.to_datetime(['2011-07-05'])
    t_2h = pd.to_datetime(['2011-07-15']) 
    
    list_data = [] 
    for  tr in range(len(t_1h)):       
        period = pd.date_range(t_1h[tr], t_2h[tr], freq = '1H') 
        
        if input_region == '1':    # Parc                             
            lh = df_fluxnet['LE'][period]            
            sh = df_euronet['H'][period]
        elif input_region == '2': # Linden
            lh = df_in_situ['LatHeat'][period]
            sh = df_in_situ['SensHeat'][period]             
        else: # Lindenberg
            lh = df_in_situ['LHFL_1'][period]
            sh = df_in_situ['SHFL_1'][period]            
            
    
        # Create a new dataframe with GLEAM, FLUXNET and EURONET data
        df_obs = pd.concat([lh, sh], axis = 1)
    
        # Rename columnsin dataframe with observations
        df_obs.columns = ['LE', 'H']    
        
        
        time_step = '1H'

        
        cclm_ref  = csm_data.get_timeseries(df_cclm_ref , clm_name, period, time_step)
        cclm_v35  = csm_data.get_timeseries(df_cclm_v35 , clm_name, period, time_step)
        cclm_v45  = csm_data.get_timeseries(df_cclm_v45 , clm_name, period, time_step)
        cclm_v45e = csm_data.get_timeseries(df_cclm_v45e, clm_name, period, time_step)
    
    
  

        for i in range(len(clm_name)):
            plot_u = vsp.get_u(cclm_ref   , cclm_v35 , cclm_v45 , cclm_v45e,  df_obs,  
                               clm_name[i], name_2[i], data_exit, y_min[i], y_max[i],
                               y_step[i]  , input_region        )

#------------------------------------------------------------------------------
# Heat wave
#------------------------------------------------------------------------------
elif mode == 5:
    #--------------------------------------------------------------------------
    # Get heat waves 
    #--------------------------------------------------------------------------
    def extreme_data(data):
        t2m_mean = data.mean()
        t2m_std  = data.std()
        
        # Create a nan timeseries
        ts_data    = pd.Series(np.nan, index = data.index)
        hot_point  = pd.Series(np.nan, index = data.index)
        cold_point = pd.Series(np.nan, index = data.index)    
    
        for i in range(len(data)):
            ts_data[i] = (data[i] - t2m_mean) / t2m_std 
        
        return ts_data, hot_point, cold_point


    cosmo_mode = True
    time_step  = '1M'
    cosmo_old  = mf_com + 'COSMO/OLD_data/PARC/CTR/' 
    
    # Create time period
    time_start = pd.to_datetime(['2010-01-01'   ])
    time_stop  = pd.to_datetime(['2015-12-31 23'])
    
    for index in range(len(time_start)):
        hourly_period = pd.date_range(time_start[index], 
                                       time_stop[index], freq = 'H')           # hourly timesteps 
        daily_period  = pd.date_range(time_start[index], 
                                       time_stop[index], freq = 'D')           # dayly timesteps   
     
        if cosmo_mode == True:
            df_old        = csm_data.cosmo_data(cosmo_old, fn_cosmo, clm_name) # Get COSMO_ref  data
            df_cosmo_data = csm_data.get_timeseries(df_old, clm_name,
                                                    hourly_period, time_step)        
            # Get COSMO data
            extrem, super_hot, super_col = extreme_data(df_cosmo_data['T_2M'])
            
        else:     
            df_hyras_data = df_hyras.resample(time_step).mean()
            # Get Hyras data
            extrem, super_hot, super_col = extreme_data(df_hyras_data['T_2M'])         
                 
        for i in range(len(extrem)): 
            if extrem[i] > 1.5:
                super_hot[i] = extrem[i]           
            elif extrem[i] < -1.5:
                super_col[i] = extrem[i]         
            else:
                super_hot[i] = np.nan 
                super_col[i] = np.nan 
        
        
        time_int_1 = str(time_start[index])[0:4]                                  # The date of period start --> need only for print
        time_int_2 =  str(time_stop[index])[0:4]
        name_plot  = f'from {time_int_1} to {time_int_2}'
        
        verf_plot = vsp.plot_waves(extrem, super_hot, super_col, name_plot, domain,
                                   station_plot, time_start[index], time_stop[index], 
                                   data_exit, cosmo_mode)    
    
#------------------------------------------------------------------------------
# Statistic analysis
#------------------------------------------------------------------------------                           
elif mode == 6:

    # Create time period
    t_1_m = pd.to_datetime(['2010-01-01'])
    t_2_m = pd.to_datetime(['2015-12-31'])
    
    period    = pd.date_range(t_1_m[0], t_2_m[0], freq = '1H') 
    period_GL = pd.date_range(t_1_m[0], t_2_m[0], freq = '1D')
    
    time_step = '1D'
    
    cclm_ref  = csm_data.get_timeseries(df_cclm_ref , clm_name, period, time_step)  
    cclm_v35  = csm_data.get_timeseries(df_cclm_v35 , clm_name, period, time_step)
    cclm_v45  = csm_data.get_timeseries(df_cclm_v45 , clm_name, period, time_step)
    cclm_v45e = csm_data.get_timeseries(df_cclm_v45e, clm_name, period, time_step)
    
    # Get COSMO data           
    cclm_ref  = cclm_ref.interpolate()
    cclm_v35  = cclm_v35.interpolate()
    cclm_v45  = cclm_v45.interpolate()
    cclm_v45e = cclm_v45e.interpolate()
    
    #Get Hyras data
    t2m  = df_hyras['T_2M'][period_GL].resample(time_step).mean()
    tmax = df_hyras['T_MAX'][period_GL].resample(time_step).mean()
    tmin = df_hyras['T_MIN'][period_GL].resample(time_step).mean()
    ts   = df_hyras['T_S'][period_GL].resample(time_step).mean()
    
    # Get GLEAM v3.5a data
    gl_Epa = df_v35a['Ep'][period_GL].resample(time_step).mean()  
    gl_Eta = df_v35a['Et'][period_GL].resample(time_step).mean()
    # Get GLEAM v3.5b data    
    gl_Epb = df_v35b['Ep'][period_GL].resample(time_step).mean()  
    gl_Etb = df_v35b['Et'][period_GL].resample(time_step).mean()  

    if input_region == '1':
        # Parc
        lh_stat = df_fluxnet['LE'][period].resample(time_step).mean()
        sh_stat = df_euronet['H'][period].resample(time_step).mean()                                   
    elif input_region == '2':
        # Linden
        lh_stat = df_in_situ['LatHeat'][period].resample(time_step).mean()
        sh_stat = df_in_situ['SensHeat'][period].resample(time_step).mean()            
    else:
        # Lindenberg
        lh_stat = df_in_situ['LHFL_1'][period].resample(time_step).mean()
        sh_stat = df_in_situ['SHFL_1'][period].resample(time_step).mean()   
              
    
    # Statistic for COSMO_CTR according to in-situ, reanalysis and satellite data
    t2m_st_orig      = isd.stat_tepm(cclm_ref['T_2M']   , t2m   , 'CCLMref_T2M'       )
    tmax_st_orig     = isd.stat_tepm(cclm_ref['TMAX_2M'], tmax  , 'CCLMref_TMAX'      )
    tmin_st_orig     = isd.stat_tepm(cclm_ref['TMIN_2M'], tmin  , 'CCLMref_TMIN'      )
    ts_st_orig       = isd.stat_tepm(cclm_ref['T_S']    , ts    , 'CCLMref_TS'        )
    aevap_st_orig_a  = isd.stat_tepm(cclm_ref['AEVAP_S'], gl_Eta, 'CCLMref_Eta'       ) 
    aevap_st_orig_b  = isd.stat_tepm(cclm_ref['AEVAP_S'], gl_Etb, 'CCLMref_Etb'       )  
    zverbo_st_orig_a = isd.stat_tepm(cclm_ref['ZVERBO'] , gl_Epa, 'CCLMref_Epa'       ) 
    zverbo_st_orig_b = isd.stat_tepm(cclm_ref['ZVERBO'] , gl_Epb, 'CCLMref_Epb'       ) 
    ashfl_st_orig    = isd.stat_tepm(cclm_ref['ASHFL_S'], sh_stat,'CCLMref_ASHFL_FL'  )
    alhfl_st_orig    = isd.stat_tepm(cclm_ref['ALHFL_S'], lh_stat,'CCLMref_ALHFL_EU'  )
    # Statistic for COSMO_v3.5 according to in-situ, reanalysis and satellite data
    t2m_st_35        = isd.stat_tepm(cclm_v35['T_2M']    , t2m   , 'CCLMv3.5_T2M'     )
    tmax_st_35       = isd.stat_tepm(cclm_v35['TMAX_2M'] , tmax  , 'CCLMv3.5_TMAX'    )
    tmin_st_35       = isd.stat_tepm(cclm_v35['TMIN_2M'] , tmin  , 'CCLMv3.5_TMIN'    )
    ts_st_35         = isd.stat_tepm(cclm_v35['T_S']     , ts    , 'CCLMv3.5_TS'      )
    aevap_st_35_a    = isd.stat_tepm(cclm_v35['AEVAP_S'] , gl_Eta, 'CCLMv3.5_Eta'     )
    aevap_st_35_b    = isd.stat_tepm(cclm_v35['AEVAP_S'] , gl_Etb, 'CCLMv3.5_Etb'     )
    zverbo_st_35_a   = isd.stat_tepm(cclm_v35['ZVERBO']  , gl_Epa, 'CCLMv3.5_Epa'     )
    zverbo_st_35_b   = isd.stat_tepm(cclm_v35['ZVERBO']  , gl_Epb, 'CCLMv3.5_Epb'     )
    ashfl_st_35      = isd.stat_tepm(cclm_v35['ASHFL_S'] , sh_stat,'CCLMv3.5_ASHFL_FL')
    alhfl_st_35      = isd.stat_tepm(cclm_v35['ALHFL_S'] , lh_stat,'CCLMv3.5_ALHFL_FL')
    # Statistic for COSMO_v4.5 according to in-situ, reanalysis and satellite data
    t2m_st_45       = isd.stat_tepm(cclm_v45['T_2M']    , t2m   , 'CCLMv4.5_T2M'      )
    tmax_st_45      = isd.stat_tepm(cclm_v45['TMAX_2M'] , tmax  , 'CCLMv4.5_TMAX'     )
    tmin_st_45      = isd.stat_tepm(cclm_v45['TMIN_2M'] , tmin  , 'CCLMv4.5_TMIN'     )
    ts_st_45        = isd.stat_tepm(cclm_v45['T_S']     , ts    , 'CCLMv4.5_TS'       )
    aevap_st_45_a   = isd.stat_tepm(cclm_v45['AEVAP_S'] , gl_Eta, 'CCLMv4.5_Eta'      )
    aevap_st_45_b   = isd.stat_tepm(cclm_v45['AEVAP_S'] , gl_Etb, 'CCLMv4.5_Etb'      )
    zverbo_st_45_a  = isd.stat_tepm(cclm_v45['ZVERBO']  , gl_Epa, 'CCLMv4.5_Epa'      )
    zverbo_st_45_b  = isd.stat_tepm(cclm_v45['ZVERBO']  , gl_Epb, 'CCLMv4.5_Epb'      )
    ashfl_st_45     = isd.stat_tepm(cclm_v45['ASHFL_S'] , sh_stat,'CCLMv4.5_ASHFL_FL' )
    alhfl_st_45     = isd.stat_tepm(cclm_v45['ALHFL_S'] , lh_stat,'CCLMv4.5_ALHFL_FL' )
    # Statistic for COSMO_v4.5e according to in-situ, reanalysis and satellite data
    t2m_st_45e      = isd.stat_tepm(cclm_v45e['T_2M']   , t2m   , 'CCLMv4.5e_T2M'     )
    tmax_st_45e     = isd.stat_tepm(cclm_v45e['TMAX_2M'], tmax  , 'CCLMv4.5e_TMAX'    )
    tmin_st_45e     = isd.stat_tepm(cclm_v45e['TMIN_2M'], tmin  , 'CCLMv4.5e_TMIN'    )
    ts_st_45e       = isd.stat_tepm(cclm_v45e['T_S']    , ts    , 'CCLMv4.5e_TS'      )
    aevap_st_45e_a  = isd.stat_tepm(cclm_v45e['AEVAP_S'], gl_Eta, 'CCLMv4.5e_Eta'     )
    aevap_st_45e_b  = isd.stat_tepm(cclm_v45e['AEVAP_S'], gl_Etb, 'CCLMv4.5e_Etb'     )
    zverbo_st_45e_a = isd.stat_tepm(cclm_v45e['ZVERBO'] , gl_Epa, 'CCLMv4.5e_Epa'     )
    zverbo_st_45e_b = isd.stat_tepm(cclm_v45e['ZVERBO'] , gl_Epb, 'CCLMv4.5e_Epb'     )
    ashfl_st_45e    = isd.stat_tepm(cclm_v45e['ASHFL_S'], sh_stat,'CCLMv4.5e_ASHFL_FL')
    alhfl_st_45e    = isd.stat_tepm(cclm_v45e['ALHFL_S'], lh_stat,'CCLMv4.5e_ALHFL_FL')
    
    df_stat_temp = pd.concat([t2m_st_orig       , t2m_st_35       , t2m_st_45       , t2m_st_45e       ,
                              tmax_st_orig      , tmax_st_35      , tmax_st_45      , tmax_st_45e      ,
                              tmin_st_orig      , tmin_st_35      , tmin_st_45      , tmin_st_45e      ,
                              ts_st_orig        , ts_st_35        , ts_st_45        , ts_st_45e        ,
                              aevap_st_orig_a   , aevap_st_35_a   , aevap_st_45_a   , aevap_st_45e_a   ,
                              aevap_st_orig_b   , aevap_st_35_b   , aevap_st_45_b   , aevap_st_45e_b   ,
                              zverbo_st_orig_a  , zverbo_st_35_a  , zverbo_st_45_a  , zverbo_st_45e_a  ,
                              zverbo_st_orig_b  , zverbo_st_35_b  , zverbo_st_45_b  , zverbo_st_45e_b  ,
                              ashfl_st_orig     , ashfl_st_35     , ashfl_st_45     , ashfl_st_45e     ,
                              alhfl_st_orig     , alhfl_st_35     , alhfl_st_45     , alhfl_st_45e    ], axis = 0)

    df_stat_temp.to_excel(data_exit + 'temp_stat.xlsx', float_format='%.3f')    
    
    
    # Statistical analysis accrding to COSMO data    
    df_cosmo_stat_v35  = csm_data.stat_cosmo(clm_name, cclm_ref, cclm_v35 )
    df_cosmo_stat_v45  = csm_data.stat_cosmo(clm_name, cclm_ref, cclm_v45 )
    df_cosmo_stat_v45e = csm_data.stat_cosmo(clm_name, cclm_ref, cclm_v45e)
    
    df_stat_cosmo = pd.concat([df_cosmo_stat_v35, df_cosmo_stat_v45, df_cosmo_stat_v45e], axis = 0)
    df_stat_cosmo.to_excel(data_exit + 'COSMO_stat.xlsx', float_format='%.3f')
    
#------------------------------------------------------------------------------
# Section: Statistic analysis (field data)
#------------------------------------------------------------------------------    
elif mode == 7:

    df_stat_list = []
    for param in par_list:

        #----------------------------------------------------------------------
        # Section 1: Run KGE and RMSD statistic analysis
        #----------------------------------------------------------------------     
        kge_res, rmsd_res, cor_res =  stf.KGE_RMSD_analysis(sf_field_stat, fn_region, 
                                                            param, refer,
                                                            ds_name, vrs_GLEAM)
        #----------------------------------------------------------------------
        # Section 2: Run DAV statistic analysis
        #----------------------------------------------------------------------
        dav_res = stf.DAV_analysis(sf_field_stat, fn_region, param, refer, ds_name, vrs_GLEAM)    
        #----------------------------------------------------------------------
        # Section 3: Import results to excel
        #----------------------------------------------------------------------
              
        STAT_result ={'Unit' : param, 'KGE' : kge_res, 'RMSD' : rmsd_res, 'CORR' : cor_res, 'DAV' : dav_res}
    
    
        df_stat = pd.DataFrame(list(STAT_result.items()), columns = ['Parameter','Values'])
        #df_stat.to_excel(path_exit + 'Statistic_' + par_list[i] + '_' + ds_name + '.xlsx',  float_format='%.3f')
        
        
        df_stat_list.append(df_stat)
    
    
 
    df_statistic = pd.concat(df_stat_list, axis = 1)
 
    df_statistic.to_excel(path_exit + 'Statistic_' + ds_name + '_' + domain + '.xlsx',  float_format='%.3f')
        #df_stat.to_excel(path_exit + 'Statistic_' + par_list[i] + '_' + ds_name + '.xlsx',  float_format='%.3f')

#------------------------------------------------------------------------------
# Plot Taylor diagram based on Yannick Copin example
#------------------------------------------------------------------------------
elif mode == 8:
 
    """
    Example of use of TaylorDiagram. Illustration dataset courtesy of Michael
    Rawlins.
    Rawlins, M. A., R. S. Bradley, H. F. Diaz, 2012. Assessment of regional climate
    model simulation estimates over the Northeast United States, Journal of
    Geophysical Research (2012JGRD..11723112R).
    """
    
    
    
    # Reference std
    stdrefs = dict(tot_prec = 1.0)
    
    # Sample std,rho: Be sure to check order and that correct numbers are placed!
    #                           stddev  corrcoef    name   
    samples = dict(tot_prec = [[0.644,   0.996,    "COSMO_ORIG" ],
                               [0.649,   0.996,    "COSMO_v3.5" ],
                               [0.648,   0.996,    "COSMO_v4.5" ],
                               [0.651,   0.996,    "COSMO_v4.5e"]])


    # Colormap (see http://www.scipy.org/Cookbook/Matplotlib/Show_colormaps)
    colors = plt.matplotlib.cm.Set1(np.linspace(0, 1, len(samples['tot_prec']) ) )
    
    # Here set placement of the points marking 95th and 99th significance
    # levels. For more than 102 samples (degrees freedom > 100), critical
    # correlation levels are 0.195 and 0.254 for 95th and 99th
    # significance levels respectively. Set these by eyeball using the
    # standard deviation x and y axis.
    
    x95 = [0.01, 0.6] # For Tair, this is for 95th level (r = 0.195)
    y95 = [0.0, 3.4]
    x99 = [0.01, 0.9] # For Tair, this is for 99th level (r = 0.254)
    y99 = [0.0, 3.4]
    
    #x95 = [0.05, 13.9] # For Prcp, this is for 95th level (r = 0.195)
    #y95 = [0.0 , 72.0]
    #x99 = [0.05, 19.0] # For Prcp, this is for 99th level (r = 0.254)
    #y99 = [0.0 , 72.0]
    
    rects = dict(tot_prec = 111)
    
    fig = plt.figure(figsize=(11,8))
    fig.suptitle("Air tepmerature (T2_M)", size='x-large')
    
    for season in ['tot_prec']:
        
        dia = vsp.TaylorDiagram(stdrefs[season], fig = fig, rect = rects[season],
                            label = 'HYRAS')
    
        dia.ax.plot(x95, y95, color = 'k')
        dia.ax.plot(x99, y99, color = 'k')
    
        # Add samples to Taylor diagram
        for i, (stddev, corrcoef, name) in enumerate(samples[season]):
            
            dia.add_sample(stddev, corrcoef,
                           #marker ='$%d$' % (i + 1), ms = 16, ls = '',
                           marker ='o', ms = 5, ls = '',
                           #mfc='k', mec='k', # B&W
                           mfc = colors[i], mec = colors[i], # Colors
                           label = name)
    
        # Add RMS contours, and label them
        contours = dia.add_contours(levels = 5, colors = '0.5') # 5 levels
        dia.ax.clabel(contours, inline = 1, fontsize = 16, fmt='%.1f')
        # Tricky: ax is the polar ax (used for plots), _ax is the
        # container (used for layout)
        #dia._ax.set_title(season)
    
    # Add a figure legend and title. For loc option, place x,y tuple inside [ ].
    # Can also use special options here:
    # http://matplotlib.sourceforge.net/users/legend_guide.html
    
    fig.legend(dia.samplePoints,
               [ p.get_label() for p in dia.samplePoints ],
               numpoints = 1, prop = dict(size = 'xx-large'), loc = 'upper right')
    
    fig.tight_layout()
    
    
    plt.savefig(path_exit + 'taylor_diagram' + '.png', format='png', dpi = 300) 
    #plt.show()
    
    

elif mode == 9:                                                                # Get avarage daily values (climatic)
    # Create time period
    time_start = pd.to_datetime(['2010-07-01'   , '2011-07-01'   , '2012-07-01 '  , 
                                 '2013-07-01'   , '2014-07-01'   , '2015-07-01'   ])
    
    time_stop  = pd.to_datetime(['2010-07-30 23', '2011-07-30 23', '2012-07-30 23', 
                                 '2013-07-30 23', '2014-07-30 23', '2015-07-30 23'])  
    
    t_start = 6                                                              # parameter --> from  
    t_stop  = 18                                                             # parameter --> to  
    active_time = True
    #--------------------------------------------------------------------------
    # Create time periods 
    #--------------------------------------------------------------------------
    periods_hour = []
    periods_days = [] 
    periods_cosmo = []
    
    for time_index in range(len(time_start)):
        hourly_period = pd.date_range(time_start[time_index],
                                      time_stop[time_index], freq = 'H')       # hourly timesteps
        
        daily_period  = pd.date_range(time_start[time_index],
                                      time_stop[time_index], freq = 'D')       # dayly timesteps 
        
        # General time period for COSMO, FLUXNET and EURONET data
        res_period    = [x for x in hourly_period if x.hour >= t_start and x.hour <= t_stop]
             
        periods_hour.append(hourly_period)
        periods_days.append(daily_period)
        periods_cosmo.append(res_period)    
    
    time_step     = 'D' 

    # Get COSMO data for full dayvalues
    cclm_ref  = csm_data.data4month(df_cclm_ref , clm_name, periods_hour, time_step) 
    cclm_v35  = csm_data.data4month(df_cclm_v35 , clm_name, periods_hour, time_step) 
    cclm_v45  = csm_data.data4month(df_cclm_v45 , clm_name, periods_hour, time_step) 
    cclm_v45e = csm_data.data4month(df_cclm_v45e, clm_name, periods_hour, time_step) 

    # Get COSMO RSTOM data only from 6:00 to 18:00
    cclm_ref_rstom  = csm_data.data4month(df_cclm_ref , clm_name, periods_cosmo, time_step) 
    cclm_v35_rstom  = csm_data.data4month(df_cclm_v35 , clm_name, periods_cosmo, time_step) 
    cclm_v45_rstom  = csm_data.data4month(df_cclm_v45 , clm_name, periods_cosmo, time_step) 
    cclm_v45e_rstom = csm_data.data4month(df_cclm_v45e, clm_name, periods_cosmo, time_step)    
    
    # Get Hyras data
    t2m   = flnt.data4month(df_hyras['T_2M'] , 'HYRAS', time_start, time_stop, time_step)  
    tmax  = flnt.data4month(df_hyras['T_MAX'], 'HYRAS', time_start, time_stop, time_step).drop(['index'], axis = 1)
    tmin  = flnt.data4month(df_hyras['T_MIN'], 'HYRAS', time_start, time_stop, time_step).drop(['index'], axis = 1)
    tsurf = flnt.data4month(df_hyras['T_S']  , 'HYRAS', time_start, time_stop, time_step).drop(['index'], axis = 1)   

    # Get GLEAM v3.5a data    
    ep_v35a = flnt.data4month(df_v35a['Ep']  , 'GLEAM', time_start, time_stop, time_step).drop(['index'], axis = 1)
    et_v35a = flnt.data4month(df_v35a['Et']  , 'GLEAM', time_start, time_stop, time_step).drop(['index'], axis = 1)  
      
    # Get GLEAM v3.5b data    
    ep_v35b = flnt.data4month(df_v35b['Ep']  , 'GLEAM', time_start, time_stop, time_step).drop(['index'], axis = 1)
    et_v35b = flnt.data4month(df_v35b['Et']  , 'GLEAM', time_start, time_stop, time_step).drop(['index'], axis = 1)

    # Get FLUXNET and EURONET data
    if input_region == '1':                                                    # Parc domain
        lh = flnt.data4month(df_fluxnet['LE'], 'FLUX', time_start, time_stop, time_step).drop(['index'], axis = 1)
        sh = flnt.data4month(df_euronet['H'] , 'EURO', time_start, time_stop, time_step).drop(['index'], axis = 1)
    elif input_region == '2':                                                  # Linden domain
        lh = flnt.data4month(df_in_situ['LatHeat'] , 'FLUX', time_start, time_stop, time_step).drop(['index'], axis = 1)
        sh = flnt.data4month(df_in_situ['SensHeat'], 'FLUX', time_start, time_stop, time_step) .drop(['index'], axis = 1)
    else:                                                                      # Lindenberg domain
        lh = flnt.data4month(df_in_situ['LHFL_1']  , 'FLUX', time_start, time_stop, time_step).drop(['index'], axis = 1)
        sh = flnt.data4month(df_in_situ['SHFL_1']  , 'FLUX', time_start, time_stop, time_step).drop(['index'], axis = 1)      


    
    label = ['2010', '2011','2012','2013','2014', '2015', '2016' ]
    lb_name = 'July'
    
    
    text_values = []
    for name in label:
        text_values.append(f'{lb_name}\n{name}')
 
     

    fig = plt.figure(figsize = (14,10))
        
    #Задание координатной сетки и места где будут располагаться графики
    egrid = (3,4)
    ax1 = plt.subplot2grid(egrid, (0,0), colspan = 4)
    ax2 = plt.subplot2grid(egrid, (1,0), colspan = 4)
    ax3 = plt.subplot2grid(egrid, (2,0), colspan = 4)
    #ax4 = plt.subplot2grid(egrid, (3,0), colspan = 4)

    if active_time == True:
        rstom = vsp.get_data_m(ax1, cclm_ref_rstom[clm_name[3]],  cclm_v35_rstom[clm_name[3]],
                                    cclm_v45_rstom[clm_name[3]], cclm_v45e_rstom[clm_name[3]], 
                                    et_v35a, et_v35b, t2m,
                                    clm_name[3],name_2[3], input_region, y_min[3],
                                    y_max[3]  , y_step[3], time_step, 
                                    text_values, settings = False, legendary = False)
    else:
        rstom = vsp.get_data_m(ax1, cclm_ref[clm_name[3]],  cclm_v35[clm_name[3]],
                                    cclm_v45[clm_name[3]], cclm_v45e[clm_name[3]], 
                                    et_v35a, et_v35b, t2m,
                                    clm_name[3],name_2[3], input_region, y_min[3],
                                    y_max[3]  , y_step[3], time_step, 
                                    text_values, settings = False, legendary = False)
    
    zverbo = vsp.get_data_m(ax2,cclm_ref[clm_name[4]],  cclm_v35[clm_name[4]],
                                cclm_v45[clm_name[4]], cclm_v45e[clm_name[4]],
                                ep_v35a, ep_v35b, t2m,
                                clm_name[4],name_2[4], input_region, y_min[4],
                                y_max[4]  , y_step[4], time_step,
                                text_values, settings = False )
    
    aevap = vsp.get_data_m(ax3, cclm_ref[clm_name[0]],  cclm_v35[clm_name[0]],
                                cclm_v45[clm_name[0]], cclm_v45e[clm_name[0]], 
                                et_v35a, et_v35b, t2m,
                                clm_name[0],name_2[0], input_region, y_min[0],
                                y_max[0]  , y_step[0], time_step, 
                                text_values, legendary = False)
        

    
    plt.savefig(data_exit + 'test/' + f'July_{time_step}mean.png', format = 'png', dpi = 300)
    plt.close(fig)        
    plt.gcf().clear()
    
    """
    for i in range(len(clm_name)):
        plot = vsp.get_data_m(cclm_ref   , cclm_v35 , cclm_v45, cclm_v45e, df_obs,
                              clm_name[i], name_2[i], input_region, y_min[i], y_max[i] , y_step[i]  ,
                              text_values, data_exit ) 
    """    
                              



        

    











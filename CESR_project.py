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

# Special function for FLUXNET and EURONET data corrections
def get_ts(data_series, period, timestep, name, change_on):
    try:
        data = data_series[period].resample(timestep).mean() 
        return data
    except KeyError as error:
        print(f'No {name} for this time period')          
        data = change_on    
        return data


#------------------------------------------------------------------------------
# Section for logical data types ----> Don't change them
#------------------------------------------------------------------------------
ldaily   = True                                                                # hour  data timestep                                                      
lperiod  = True                                                                # daily data timestep                                                          
llperiod = True                                                                # user  data timestep                                                                                                               

#------------------------------------------------------------------------------
# Section: Constant parameters
#------------------------------------------------------------------------------
t0melt = 273.15                                                                


#------------------------------------------------------------------------------
# Section for users: Parameters can be changed by user
#------------------------------------------------------------------------------                                  

#------------------------------------------------------------------------------
# Parameters for: period_cal    --> timestep of data (1 - hourly, 
#                                                     2 - Montly,
#                                                     3 - User interval)
#
#    
#             input_region      --> (P - park,
#                                    L - linden,
#                                    Li - lindenberg)
# 
#             input_station     --> (For Park region --> RuR --> 'Rollesbroich      (lat - 50.62; lon - 6.30; Land type - Grass)
#                                                        RuS --> 'Selhausen Juelich (lat - 50.86; lon - 6.44; Land type - Crops) 
#                                                        SeH --> 'Selhausen         (lat - 50.87; lon - 6.44; Land type - Agricultural area)
#                                    For Linden      --> LiN --> 'Linden'           (lat - ; lon - ; Land type - Grass)
#                                    For Lindenberg  --> LiD --> 'Lindenberg'       (lat - ; lon - ; Land type - ))
#           
#             time_array        --> time step for resample initial dataframe
#                                     period_cal = 1 then time_array = 'H'
#                                     period_cal = 2 then time_array = 'D'
#                                     period_cal = 3 then time_array = '2D'   
#------------------------------------------------------------------------------
period_cal    = '3'               
input_region  = 'P'
input_station = 'RuR'           
time_array   = ['H', 'D', '5D']

#------------------------------------------------------------------------------
# Define paths for data
#------------------------------------------------------------------------------    

mf_com    = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'                        # The main paths which are general for all data

path_exit = mf_com + 'Python_results/'                                         # The path for results

 
if input_region == 'P':                                                        # Special parameters for Parc domain
    print('The Parc domain was chosen: \n')     
    sf_region = 'PARC/'                                                        # folder with data for Parc domain  
    fn_region = 'parc'                                                         # filename part 
               
elif input_region == 'L':                                                      # Special parameters for Linden domain
    print('The Linden domain was chosen: \n')
    sf_region = 'LINDEN/'                                                     
    fn_region = 'linden'                                                  
    
elif input_region == 'Li':                                                     # Special parameters for Lindenberg domain
    print('The Lindenberg domain was chosen: \n')
    sf_region = 'LINDENBERG/'                                                 
    fn_region = 'lindenberg'                                                
else:
    print ('Error: No data for domain --> line 161')


sf_cclm_ref   = mf_com + 'COSMO/' + sf_region + 'CTR/'                         # COSMO_CTR
sf_cclm_v35   = mf_com + 'COSMO/' + sf_region + 'v3.5/'                        # COSMO_v3.5
sf_cclm_v45   = mf_com + 'COSMO/' + sf_region + 'v4.5/'                        # COSMO_v4.5
sf_cclm_v45e  = mf_com + 'COSMO/' + sf_region + 'v4.5e/'                       # COSMO_v4.5e

sf_fluxnet    = mf_com + 'IN-SITU/FLUXNET/'                                    # FLUXNET data    
sf_euronet    = mf_com + 'IN-SITU/EURONET/'                                    # EURONET data
sf_linden     = mf_com + 'IN-SITU/LINDEN/'                                     # Linden  data 
sf_lindenberg = mf_com + 'IN-SITU/LINDENBERG/'                                 # Lindenberg  data 

sf_eobs       = mf_com +'REANALYSIS/EOBS/'                                     # EOBS data
sf_hyras      = mf_com +'REANALYSIS/HYRAS/'                                    # HYRAS data
sf_gleam      = mf_com +'REANALYSIS/GLEAM/'                                    # GLEAM data  

fn_cosmo      = '_ts_mean_1999_2015.csv'                                       # General part in file name for COSMO and experiments


#------------------------------------------------------------------------------ 
# Names of parameters for COSMO data
#------------------------------------------------------------------------------
clm_name = ['AEVAP_S'  , 'ALHFL_BS' , 'ALHFL_PL', 'ALHFL_S' , 'ASHFL_S', 
            'ZTRALEAV' , 'ZTRANG'   , 'ZTRANGS' , 'ZVERBO'  , 'QV_2M'  , 
            'QV_S'     , 'RELHUM_2M', 'RSTOM'   , 'T_2M'    , 'T_S'    ,
            'PS'       ]

#------------------------------------------------------------------------------
# Names of plot labels
#------------------------------------------------------------------------------
name_1 = ['Amount of water evaporation (surface) - AEVAP_S'                ,
          'Average latent heat flux from bare soil evaporation - ALHFL_BS' ,
          'Average latent heat flux from plants - ALHFL_PL'                ,
          'Average latent heat flux (surface) - ALHFL_S'                   ,
          'Average sensible heat flux (surface) - ASHFL_S'                 ,
          'Transpiration rate of dry leaves - ZTRALEAV'                    ,
          'Transpiration contribution by the first layer - ZTRANG'         ,
          'Total transpiration - ZTRANGS'                                  ,
          'Total evapotranspiration - ZVERBO'                              , 
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
name_2   = ['AEVAP\u209B, kg m \u207b\u00B2'     , 'ALHFL_BS, W m \u207b\u00B2'        ,
            'ALHFL\u209A\u2097, W m \u207b\u00B2', 'ALHFL\u209B, W m \u207b\u00B2'     , 
            'ASHFL\u209B, W m \u207b\u00B2'      , 'ZTRALEAV, mm day \u207b\u00B9'     ,
            'ZTRANG, mm day \u207b\u00B9'        , 'ZTRANGS, mm day \u207b\u00B9'      ,
            'ZVERBO, mm day \u207b\u00B9'        , 'QV\u2082\u2098, kg kg \u207b\u00B9',
            'QV\u209B, kg kg \u207b\u00B9'       , 'RH\u2082\u2098, %'                 ,
            'RSTOM, s m \u207b\u00B9'            , 'T\u2082\u2098, C \u2070'           ,
            'T\u209B, C \u2070'                  , 'PS, hPa'                           ] 
                       
#------------------------------------------------------------------------------
# Select actual limits for plots arrording to timestep   
#------------------------------------------------------------------------------
if period_cal == '1':                                                          # DAILY data with hourly timesteps       
    print(f'Data format - daily data, Timestep - {time_array[0]}')       
    # Logical types for data
    daily_time_step   = True                                                   
    monthly_time_step = False     
    long_time_step    = False  
    # Time step
    ts                = time_array[0]  
    # Lower limit
    y_min  = [  -0.05,    -5.0,    -5.0,    -25.0   ,    0.0     ,     0.0,    # AEVAP  , ALHFL_BS, ALHFL_PL, ALHFL_S, ASHFL_S, AZTRALEAV,
                 0.0 ,     0.0,     0.0,      0.0   ,   -2.0     ,    30.0,    # AZTRANG, AZTRANGS,  AZVERBO,   QV_2M,    QV_S, RELHUM_2M,  
                 0.0 ,   -15.0,   -15.0,    900.0                         ]    # RSTOM  ,     T_2M,      T_S,      PS 
    # Upper limit
    y_max  = [   0.41,    50.1,    50.1,    250.1   ,  250.1     ,    50.1,    
                50.1 ,    50.1,    50.0,      0.0151,    2.01    ,   100.1,     
              5001.0 ,    35.1,    35.0,   1050.1                         ]    
    # Step
    y_step = [   0.05,     5.0,     5.0,     25.0   ,   25.0     ,    10.0,    
                10.0 ,    10.0,    10.0,      0.005 ,    0.5     ,    10.0,    
               500.0 ,    10.0,    10.0,     25.0                         ]    

elif period_cal == '2':                                                        # MONTLY data with daily timesteps    
    print(f'Data format - daily data, Timestep - {time_array[1]}')
    # Logical types for data
    daily_time_step   = False                                                  
    monthly_time_step = True 
    long_time_step    = False
    # Time step
    ts                = time_array[1]        
    # Lower limit 
    y_min = [    0.0 ,  -25.0,   -25.0,    -25.0   ,    0.0     ,     0.0,     # AEVAP  , ALHFL_BS, ALHFL_PL, ALHFL_S, ASHFL_S, AZTRALEAV,
                 0.0 ,    0.0,     0.0,      0.0   ,    0.0     ,    30.0,     # AZTRANG, AZTRANGS,  AZVERBO,   QV_2M,    QV_S, RELHUM_2M, 
                 0.0 ,  -15.0,   -15.0,    900.0                         ]     # RSTOM  ,     T_2M,      T_S,      PS 
    # Upper limit
    y_max = [    6.01,  125.1,   125.1,    125.1   ,    250.1   ,    50.1,     
                50.1 ,   50.1,    50.1,      0.0151,      0.0151,   100.1,  
             20000.1 ,   35.1,    35.0,   1050.1                         ]  
    # Step
    y_step = [   0.50,   25.0,    25.0,     25.0   ,     25.0   ,    10.0,     
                10.0 ,   10.0,    10.0,      0.005 ,      0.005 ,    10.0,      
              5000.0 ,   10.0,    10.0,     25.0                         ]     

elif period_cal == '3':                                                        # USER data with user timesteps  
    print(f'Data format - daily data, Timestep - {time_array[2]}') 
    # Logical types for data
    daily_time_step   = False                                                  
    monthly_time_step = False    
    long_time_step    = True 
    # Time step
    ts = time_array[2]
    # Lower limit
    y_min = [    0.0 ,    0.0,     0.0,      0.0   ,    -20.0   ,     0.0,     # AEVAP  , ALHFL_BS, ALHFL_PL, ALHFL_S, ASHFL_S, AZTRALEAV, 
                 0.0 ,    0.0,     0.0,      0.0   ,      0.0   ,    40.0,     # AZTRANG, AZTRANGS,  AZVERBO,   QV_2M,    QV_S, RELHUM_2M,
                 0.0 ,    5.0,     5.0,    975.0                         ]     # RSTOM  ,     T_2M,      T_S,      PS     
    # Upper limit
    y_max = [    6.1 ,   75.1,    30.1,    125.1   ,    100.1   ,     5.1,           
                 1.51,    5.1,    10.1,      0.0151,      0.0151,   100.1,       
              5000.1 ,   30.1,    35.1,   1025.1                         ]                                 
    # Step
    y_step = [   0.5 ,   15.0,     5.0,     25.0   ,     20.0   ,     1.0,           
                 0.25,    0.5,     2.0,      0.005 ,      0.005 ,    10.0,      
               500.0 ,    5.0,     5.0,     10.0                         ]                          
else:
    print ('Error: Incorrect actual period!')
    sys.exit()      

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Section: Clear the privios results
#------------------------------------------------------------------------------
while True:
    input_control = input('Do you want to remote previous data: yes - y; no - n \n') 
    if input_control == 'y':
        clean_result = stmo.dep_clean(path_exit)
        print ('All previous results were deleted: \n')        
        break
    
    elif input_control == 'n': 
        print ('All previous results were saved and ' +
               'in case of the same name - data will be rewritten: \n')
        break
    else:
        print ('Error: Incorrect format, repeat! \n')

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Get initial data: COSMO, FLUXNET, EURONET, GLEAM, HYRAS, E-OBS
#------------------------------------------------------------------------------

# The COSMO data has a hourly timestep
df_cclm_ref  = csm_data.cosmo_data(sf_cclm_ref , fn_cosmo, clm_name)
df_cclm_v35  = csm_data.cosmo_data(sf_cclm_v35 , fn_cosmo, clm_name)
df_cclm_v45  = csm_data.cosmo_data(sf_cclm_v45 , fn_cosmo, clm_name)
df_cclm_v45e = csm_data.cosmo_data(sf_cclm_v45e, fn_cosmo, clm_name)

# The FLUXNET and EURONET has a hourly timestep
df_fluxnet, station_name_plot = flnt.fluxnet_data(sf_fluxnet, input_station)   # get FLUXNET data
df_euronet                    = flnt.euronet_data(sf_euronet, input_station)   # get EORONET data      
       
# The GLEAM, E-OBS and HYRAS datasets has a daily timestep
df_eobs          = radata.eobs_data(sf_eobs, fn_region)                        # get E-OBS data
df_hyras         = radata.hyras_data(sf_hyras, fn_region)                      # get HYRAS data
df_v35a, df_v35b = radata.gleam_data(sf_gleam, fn_region)                      # get GLEAM data

#------------------------------------------------------------------------------
# Get time periods
#------------------------------------------------------------------------------
'''
# Example for several periods of time
time_id_1 = pd.to_datetime(['2010-06-01'   , '2013-06-01'   ])
time_id_2 = pd.to_datetime(['2010-08-31 23', '2013-08-31 23'])

# Additional examples for work with time
houry_time_period = pd.date_range(start = '2010-06-01', end = '2010-08-31 23', freq = 'H')
dayly_time_period = pd.date_range(start = '2010-06-01', end = '2010-08-31 23', freq = 'D')
'''

time_start = pd.to_datetime(['2010-01-01'   , '2013-01-01'   ])
time_stop  = pd.to_datetime(['2010-12-31 23', '2013-12-31 23'])

t_start = 0                                                                    # parameter --> from  
t_stop  = 23                                                                   # parameter --> to
#------------------------------------------------------------------------------
# Section: Work with data and data visualization
#------------------------------------------------------------------------------  

# Ged monthly date for time periods and plot maps
for  index in range(len(time_start)):   
    #--------------------------------------------------------------------------
    # Create time periods 
    #-------------------------------------------------------------------------- 
    hourly_period = pd.date_range(time_start[index], time_stop[index], freq = 'H')  # hourly timesteps
    daily_period  = pd.date_range(time_start[index], time_stop[index], freq = 'D')  # dayly timesteps 
    
    # General time period for COSMO, FLUXNET and EURONET data
    res_period   = [x for x in hourly_period if x.hour >= t_start and x.hour <= t_stop]

    
    #--------------------------------------------------------------------------
    # Subsection: Create data for plots
    #--------------------------------------------------------------------------

    # COSMO data --> daily mean
    cclm_ref  = csm_data.get_timeseries(df_cclm_ref , clm_name, res_period, 'D')   # CCLMref  --> original COSMO     
    cclm_v35  = csm_data.get_timeseries(df_cclm_v35 , clm_name, res_period, 'D')   # CCLMv35  --> experiment    
    cclm_v45  = csm_data.get_timeseries(df_cclm_v45 , clm_name, res_period, 'D')   # CCLMv45  --> experiment           
    cclm_v45e = csm_data.get_timeseries(df_cclm_v45e, clm_name, res_period, 'D')   # CCLMv45e --> previous version parc_v45  
    
    # Get COSMO values for 
    cclm_mean      = cclm_ref.resample(ts).mean()
    cclm_v35_mean  = cclm_v35.resample(ts).mean()
    cclm_v45_mean  = cclm_v45.resample(ts).mean()
    cclm_v45e_mean = cclm_v45e.resample(ts).mean()
    
    
    s_zero = pd.Series(-1, index = res_period)
    #FLUXNET data    
    t2m_flux = get_ts(df_fluxnet['T2m'], res_period, ts, 'T2m FLUXNET', s_zero)  
    le_flux  = get_ts(df_fluxnet['LE'] , res_period, ts, 'LE FLUXNET' , s_zero) 
    ts_flux  = get_ts(df_fluxnet['Ts'] , res_period, ts, 'Ts FLUXNET' , s_zero) 
    pa_flux  = get_ts(df_fluxnet['Pa'] , res_period, ts, 'Pa FLUXNET' , s_zero) 

    #EURONET data
    t2m_euro = get_ts(df_euronet['TA'] , res_period, ts, 'TA EURONET' , s_zero)
    le_euro  = get_ts(df_euronet['LE'] , res_period, ts, 'LE EURONET' , s_zero)
    t_s_euro = get_ts(df_euronet['TS'] , res_period, ts, 'TS EURONET' , s_zero)    
    rh_euro  = get_ts(df_euronet['RH'] , res_period, ts, 'RH EURONET' , s_zero)
    h_euro   = get_ts(df_euronet['H']  , res_period, ts, 'H EURONET'  , s_zero)
    #pa_euro  = df_euronet['PA'][res_period].resample(ts).mean() * 10.0
      
    # HYRAS data
    t2m_hyras = df_hyras['T_2M'][daily_period].resample(ts).mean()        

    #E-OBS data
    t2m_eobs  = df_eobs['T_2M'][daily_period].resample(ts).mean()       
                   
    #GLEAM data v3.5a        
    ep_v35a = df_v35a['Ep'][daily_period].resample(ts).mean()                  # Ep --> potential evaporation
    et_v35a = df_v35a['Et'][daily_period].resample(ts).mean()                  # Et --> transpiration 
   
    #GLEAM data v3.5b 
    ep_v35b = df_v35b['Ep'][daily_period].resample(ts).mean()
    et_v35b = df_v35b['Et'][daily_period].resample(ts).mean()                  
      
    #--------------------------------------------------------------------------
    # Subsection: Data vizualization - Plots for all parameters   
    #--------------------------------------------------------------------------
   
    # Additional information for plot title: General            
    time_int_1 = str(time_start[index])[0:10]                                  # The date of period start --> need only for print
    time_int_2 =  str(time_stop[index])[0:10]                                  # The date of period stop  --> need only for print
    date_ind   = f'Time step: {time_int_1} to {time_int_2}'                    # The full date of period  --> need for plot label          
    name_3     = 'Hours'                                                       # x - label for hourly plots   
    l_p        = 'upper left'                                                  # The position of legend
    nst        = station_name_plot                                             # the name of the research station

    for k in range(len(clm_name)):       
        # Create area for plot
        fig = plt.figure(figsize = (14,10))
        ax  = fig.add_subplot(111)      
        
        if clm_name[k] in ('ALHFL_BS', 'ALHFL_PL' , 'ZTRALEAV', 'ZTRANG'   ,   # Plot data parameters
                           'ZTRANGS' , 'QV_2M'    , 'QV_S'    , 'RELHUM_2M', 
                           'RSTOM'   , 'PS'                                ):
            
            print (f'Plot - {clm_name[k]}, period: {time_int_1} to {time_int_2}')
                        
            if ldaily == daily_time_step:
                plot4par = vis.plot_4d(ax, cclm_mean[clm_name[k]]    ,  cclm_v35_mean[clm_name[k]], 
                                           cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]],
                                           'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' ,
                                           name_1[k]  , name_2[k]  , name_3     , 
                                           date_ind   , nst        , l_p        ,
                                           y_min[k]   , y_max[k]   , y_step[k]  ,
                                           time_start[index]  , time_stop[index]  )                                     
            else:
                plot4par = vis.plot_4(ax, cclm_mean[clm_name[k]]    ,  cclm_v35_mean[clm_name[k]],
                                          cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]],
                                          'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' ,                                          
                                          name_1[k]  , name_2[k]  ,
                                          date_ind   , nst        , l_p        ,
                                          y_min[k]   , y_max[k]   , y_step[k]  ,
                                          time_start[index]  , time_stop[index]  )                                          
                                           
        elif clm_name[k] in ('T_2M', 'T_S'):                                   # Plot data T2M or TS
            print (f'Plot - {clm_name[k]}, period: {time_int_1} to {time_int_2}')
                                   
            if ldaily == daily_time_step:
                plot4temp = vis.plot_4d(ax, cclm_mean[clm_name[k]], cclm_v35_mean[clm_name[k]], 
                                        cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]], 
                                            'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' ,     
                                            name_1[k]  , name_2[k]  , name_3     , 
                                            date_ind   , nst        , l_p        ,
                                            y_min[k]   , y_max[k]   , y_step[k]  ,
                                            time_start[index]  , time_stop[index]  )                                                                          
            else:
                plot4temp = vis.plot_5(ax, cclm_mean[clm_name[k]], cclm_v35_mean[clm_name[k]], 
                                       cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]], t2m_hyras,  
                                           'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' , 'OBS'    ,
                                           name_1[k]  , name_2[k]  ,
                                           date_ind   , nst, l_p   ,
                                           y_min[k]   , y_max[k]   , y_step[k]  , 
                                           time_start[index]  , time_stop[index]  )           

        elif clm_name[k] in ('AEVAP_S', 'ZVERBO'):                             # Plot data AEVAP_S or ZVERBO
            print (f'Plot - {clm_name[k]}, period: {time_int_1} to {time_int_2}') 
            # Define in-situ data type
            if clm_name[k] in 'AEVAP_S':
                gleam_v35a = et_v35a
                gleam_v35b = et_v35b 
            else:
                gleam_v35a = ep_v35a  
                
                
                gleam_v35b = ep_v35b
            # -----------------------------------------------------------------
                    
            if ldaily == daily_time_step:
                plot4evap = vis.plot_4d(ax, cclm_mean[clm_name[k]], cclm_v35_mean[clm_name[k]], 
                                        cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]],
                                            'CCLMref'  ,  'CCLMv3.5',  'CCLMv4.5',  'CCLMv4.5e', 
                                            name_1[k]  ,   name_2[k],      name_3, 
                                            date_ind   ,    nst, l_p,
                                            y_min[k]   ,    y_max[k],   y_step[k],
                                            time_start[index]  ,   time_stop[index])                       
            else:
                plot4evap = vis.plot_6(ax, cclm_mean[clm_name[k]], cclm_v35_mean[clm_name[k]],
                                       cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]], gleam_v35a  , gleam_v35b  ,                                    
                                           'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' , 'GLEAM 3.5a', 'GLEAM 3.5b',                                          
                                           name_1[k]  , name_2[k]  , date_ind   , nst, l_p    ,
                                           y_min[k]   , y_max[k]   , y_step[k]  ,
                                           time_start[index]  , time_stop[index]  )                                                          
                                                          
        elif clm_name[k] in ('ALHFL_S', 'ASHFL_S'):                            # Plot data ALHFL_S or ASHFL_S
            print (f'Plot - {clm_name[k]}, period: {time_int_1} to {time_int_2}')            
            # Define in-situ data type
            if clm_name[k] in 'ALHFL_S':
                heat_flux = le_flux
            else:
                heat_flux = h_euro            
            # -----------------------------------------------------------------                 
            
            if ldaily == daily_time_step:
                plot4hf = vis.plot_5d(ax, cclm_mean[clm_name[k]], cclm_v35_mean[clm_name[k]], 
                                      cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]], heat_flux,
                                          'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' , 'OBS'    ,
                                          name_1[k]  , name_2[k]  , name_3     ,
                                          date_ind   , nst, l_p   ,
                                          y_min[k]   , y_max[k]   , y_step[k]  ,
                                          time_start[index]  , time_stop[index])                                                                  
            else:
                plot4hf = vis.plot_5(ax, cclm_mean[clm_name[k]], cclm_v35_mean[clm_name[k]],
                                     cclm_v45_mean[clm_name[k]], cclm_v45e_mean[clm_name[k]], heat_flux, 
                                         'CCLMref'  , 'CCLMv3.5' , 'CCLMv4.5' , 'CCLMv4.5e' , 'OBS'    ,                                            
                                         name_1[k]  , name_2[k]  , 
                                         date_ind   , nst, l_p   , 
                                         y_min[k]   , y_max[k]   , y_step[k]  , 
                                         time_start[index]  , time_stop[index]  )                                          
                               
       
            
        output_name = f'{clm_name[k]}_{time_int_1}_{time_int_2}.png'
            
        plt.savefig(path_exit + output_name, format = 'png', dpi = 300) 

        plt.close(fig)        
        plt.gcf().clear()  
        
                    

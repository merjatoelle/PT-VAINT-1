# -*- coding: utf-8 -*-
"""
Created on Tue May 25 13:04:49 2021

@author: churiulin
"""
import numpy as np
import pandas as pd

import fluxnet_data      as flnt                                               # personal module for IN-SITU    data (FLUXNET, EURONET)             
import cosmo_data        as csm_data                                           # personal module for MODEL      data (COSMO)
import reanalysis_data   as radata                                             # personal module for REANALISIS data (GLEAM, EOBS, HYRAS)
import vis_stat_plots    as vsp                                                # personal module for visialisation data (GLEAM, EOBS, HYRAS) 
import insitu_data       as isd


import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error



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


def stat_cosmo(df_ctr, df_mod):
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
    
    df_stat_cosmo = pd.DataFrame({'Parameter' : ['AEVAP_S','ALHFL_S','ASHFL_S','RSTOM','ZVERBO','T_2M','T_S','TMAX_2M','TMIN_2M','ZTRALEAV'],
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

mode = 7                                                                        




# Choose your region for analysis (Possible options: 1 - PARC domain
#                                                    2 - LINDEN domain
#                                                    3 - LINDENBERG domain )

input_region = '3'


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
    
    




# Path to the main project folder
mf_com    = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'
data_exit = mf_com + '/ANALYSIS/PLOTS/' + domain + '/'

#------------------------------------------------------------------------------
# Setting for COSMO data
#------------------------------------------------------------------------------

# Path to COSMO subfolders
sf_parc01_ctr     = 'COSMO/' + domain + '/CTR/'                                         
sf_parc_v35       = 'COSMO/' + domain + '/v3.5/'                                         
sf_parc_v45       = 'COSMO/' + domain + '/v4.5/'                                        
sf_parc_v45_evap  = 'COSMO/' + domain + '/v4.5e/'                                    

# Names of parameters for COSMO data
clm_name = ['AEVAP_S', 'ALHFL_S' , 'ASHFL_S', 'RSTOM'   ,
            'ZVERBO' , 'T_2M'    , 'T_S'    , 'TMAX_2M' ,
            'TMIN_2M', 'ZTRALEAV']

if mode == 3:
    name_2   = ['AEVAP_S, kg/m2', 'ALHFL_S, W/m2' , 'ASHFL_S, W/m2' , 
                'RSTOM, s/m'    , 'ZVERBO, mm/hour', 'T_2M, C'       , 
                'T_S, C'        , 'TMAX_2M, C'    , 'TMIN_2M, C'    ,
                'ZTRALEAV, mm/hour' ]
elif mode == 4:
    name_2   = ['AEVAP_S, kg/m2', 'ALHFL_S, W/m2' , 'ASHFL_S, W/m2' , 
                'RSTOM, s/m'    , 'ZVERBO, mm/hour', 'T_2M, C'       , 
                'T_S, C'        , 'TMAX_2M, C'    , 'TMIN_2M, C'    ,
                'ZTRALEAV, mm/hour' ]    
    
else:
    name_2   = ['AEVAP_S, kg/m2', 'ALHFL_S, W/m2' , 'ASHFL_S, W/m2' , 
                'RSTOM, s/m'    , 'ZVERBO, mm/day', 'T_2M, C'       , 
                'T_S, C'        , 'TMAX_2M, C'    , 'TMIN_2M, C'    ,
                'ZTRALEAV, mm/day' ]    

# Name of COSMO data
fn_cosmo = '_ts_mean_1999_2015.csv'


#------------------------------------------------------------------------------
# Setting for EURONET or FLUXNET data
#------------------------------------------------------------------------------

# Path to EURONET and FLUXNET subfolders
sf_fluxnet = 'IN-SITU/FLUXNET/'                                                # The subfolder for FLUXNET data    
sf_euronet = 'IN-SITU/EURONET/'                                                # The subfolder for EURONET data

# Version of FLUXNET data: ERAI or FULLSET
input_mode = 'FULLSET'

# EURONET or FLUXNET stations for work
mylist = ['RuR', 'RuS', 'SeH']

# Input station
input_station = 'RuR'

#------------------------------------------------------------------------------
# Settings for GLEAM data
#------------------------------------------------------------------------------

# Path to GLEAM data
sf_gleam   = 'REANALYSIS/GLEAM/'                              

# Special parameters for GLEAM data (version of GLEAM data)
lversion_a  = False                                                          
lversion_b  = False     
lversion_bt = True 


 
#------------------------------------------------------------------------------
# Settings for HYRAS and E-OBS data
#------------------------------------------------------------------------------

# Path to subfolder
sf_hyras = 'REANALYSIS/HYRAS/'
sf_eobs  = 'REANALYSIS/EOBS/'

# Types of parameters for analysis
parameters = ['T_2M', 'T_MAX', 'T_MIN', 'T_S']







        
#------------------------------------------------------------------------------
# Additional settings (timestep and limits for y-axis for plots)
#------------------------------------------------------------------------------

# Timestep for data (need for pd.resample)
ts     = '1D'

#            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,  ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
y_min_m  = [   0.0,      0.0,    -50.0,       0.0,     0.0,    0.0,    0.0,    0.0,     0.0,    0.0 ]
y_max_m  = [  4.01,    110.1,     75.1,   20000.1,    4.01,   25.1,   25.1,   25.1,    25.1,    3.01]
y_step_m = [   0.5,     10.0,     25.0,    2000.0,     0.5,    5.0,    5.0,    5.0,     5.0,    0.5 ]  


#            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
y_min_d  = [   0.0,      0.0,    -50.0,       0.0,     0.0 ,    5.0,    5.0,    5.0,     5.0,     0.0 ]
y_max_d  = [  4.01,    150.1,     75.1,   10000.1,     6.1 ,   30.1,   30.1,   30.1,    30.1,     4.01]
y_step_d = [   0.5,     10.0,     25.0,    1000.0,     1.0 ,    5.0,    5.0,    5.0,     5.0,     0.5 ]  



#            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
y_min_h  = [   0.0,      0.0,    -50.0,       0.0,     0.0 ,   10.0,   10.0,    0.0,     0.0,     0.0]
y_max_h  = [  0.51,    250.1,    200.1,   10000.1,     8.1 ,   30.1,   30.1,   25.1,    25.1,     6.0]
y_step_h = [   0.1,     25.0,     25.0,    1000.0,     1.0 ,    2.0,    2.0,    5.0,     5.0,     1.0]  


#            AEVAP,  ALHFL_S,  ASHFL_S,     RSTOM,   ZVERBO,   T2m ,    TS ,   TMAX,    TMIN,  ZTRALEAV
y_min_u  = [   0.0,      0.0,   -100.0,       0.0,     0.0 ,   10.0,   10.0,   10.0,    10.0,     0.0]
y_max_u  = [  0.51,    325.1,    350.1,   10000.1,    15.1 ,   40.1,   40.1,   40.1,    40.1,     9.1]
y_step_u = [   0.1,     25.0,     50.0,    1000.0,     1.0 ,    5.0,    5.0,    5.0,     5.0,     1.0]  

#------------------------------------------------------------------------------
# Get initial COSMO data
#------------------------------------------------------------------------------

parc01_ctr = csm_data.cosmo_data(mf_com, sf_parc01_ctr    , fn_cosmo, clm_name)
parc_v35   = csm_data.cosmo_data(mf_com, sf_parc_v35      , fn_cosmo, clm_name)
parc_v45   = csm_data.cosmo_data(mf_com, sf_parc_v45      , fn_cosmo, clm_name)
parc_v45e  = csm_data.cosmo_data(mf_com, sf_parc_v45_evap , fn_cosmo, clm_name)

#------------------------------------------------------------------------------
# Get initial IN-CITY data based on FLUXNET and EURONET data
#------------------------------------------------------------------------------

df_fluxnet, station_name_plot = flnt.fluxnet_data(mf_com, sf_fluxnet, input_mode,
                                                  mylist, input_station)    

df_euronet = flnt.euronet_data(mf_com, sf_euronet, input_station)

#------------------------------------------------------------------------------
# Get reanalysis data based on GLEAM data
#------------------------------------------------------------------------------

df_gleam = radata.gleam_data(mf_com, sf_gleam, fn_region, 
                             lversion_a, lversion_b, lversion_bt)        


#------------------------------------------------------------------------------
# Get HYRAS and E-OBS data
#------------------------------------------------------------------------------

df_t2m_eobs = radata.eobs_data(mf_com, sf_eobs, fn_region)  

df_t2m_hyras = radata.hyras_data(mf_com, sf_hyras, parameters, fn_region)



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
    t_1_m = pd.to_datetime(['2011-01-01'])
    t_2_m = pd.to_datetime(['2015-12-31'])

    period       = pd.date_range(t_1_m[0], t_2_m[0], freq = '1H')     
    period_GLEAM = pd.date_range(t_1_m[0], t_2_m[0], freq = '1D')  
    period_HYRAS = pd.date_range(t_1_m[0], t_2_m[0], freq = '1D') 
    
    #Get Hyras data
    t2m_m  = flnt.montly_data(df_t2m_hyras['T_2M'] , period_HYRAS, ts)
    tmax_m = flnt.montly_data(df_t2m_hyras['T_MAX'], period_HYRAS, ts)
    tmin_m = flnt.montly_data(df_t2m_hyras['T_MIN'], period_HYRAS, ts)
    ts_m   = flnt.montly_data(df_t2m_hyras['T_S']  , period_HYRAS, ts)
    
    
    # Get climatic mean values for each month for GLEAM data
    gleam_Epa_m = flnt.montly_data(df_gleam['Ep_a'], period_GLEAM, ts)
    gleam_Eta_m = flnt.montly_data(df_gleam['Et_a'], period_GLEAM, ts)
    gleam_Epb_m = flnt.montly_data(df_gleam['Ep_b'], period_GLEAM, ts)
    gleam_Etb_m = flnt.montly_data(df_gleam['Et_b'], period_GLEAM, ts)
    

    if input_region == '1':
        # Parc
        lh_m = flnt.montly_data(df_fluxnet['LE'], period, ts) 
        sh_m = flnt.montly_data(df_euronet['H'] , period, ts)    
    elif input_region == '2':
        # Linden
        lh_m = flnt.montly_data(df_in_situ['LatHeat'] , period, ts)
        sh_m = flnt.montly_data(df_in_situ['SensHeat'], period, ts) 
    else:
        # Lindenberg
        lh_m = flnt.montly_data(df_in_situ['LHFL_1'], period, ts)
        sh_m = flnt.montly_data(df_in_situ['SHFL_1'], period, ts)        
          
    # Create a new dataframe with GLEAM, FLUXNET and EURONET data
    df_obs_m = pd.concat([lh_m, sh_m, gleam_Epa_m, gleam_Eta_m, 
                                      gleam_Epb_m, gleam_Etb_m,
                                      t2m_m, tmax_m, tmin_m, ts_m], axis = 1)
    
    # Rename columnsin dataframe with observations
    df_obs_m.columns = ['LE', 'H', 'Ep_a', 'Et_a', 
                                   'Ep_b', 'Et_b',
                                   'T_2M', 'TMAX', 'TMIN', 'TS'  ]
    
    
    # Get climatic mean values for each month for COSMO data
    m_cosmo_orig = csm_data.cosmo_montly_data(clm_name, parc01_ctr, period, ts )
    m_cosmo_v35  = csm_data.cosmo_montly_data(clm_name, parc_v35  , period, ts )
    m_cosmo_v45  = csm_data.cosmo_montly_data(clm_name, parc_v45  , period, ts )
    m_cosmo_v45e = csm_data.cosmo_montly_data(clm_name, parc_v45e , period, ts )
    

    # Plot parc data
    for i in range(len(clm_name)):
        plot = vsp.get_m(m_cosmo_orig, m_cosmo_v35, m_cosmo_v45, 
                         m_cosmo_v45e,    df_obs_m, clm_name[i],   name_2[i], 
                         data_exit   ,  y_min_m[i],  y_max_m[i], y_step_m[i],
                         input_region)




elif mode == 2:
    #--------------------------------------------------------------------------
    # Get avarage daily values (climatic)
    #--------------------------------------------------------------------------

    t_1_d = pd.to_datetime(['2010-06-01', '2011-06-01', '2012-06-01', 
                            '2013-06-01', '2014-06-01', '2015-06-01'])
    
    t_2_d = pd.to_datetime(['2010-06-30', '2011-06-30', '2012-06-30', 
                            '2013-06-30', '2014-06-30', '2015-06-30'])                                
    
    # Get climatic mean values for each day in June for COSMO data
    d_cosmo_orig = csm_data.cosmo_daily_data(t_1_d, t_2_d, clm_name, parc01_ctr, ts) 
    d_cosmo_v35  = csm_data.cosmo_daily_data(t_1_d, t_2_d, clm_name, parc_v35  , ts) 
    d_cosmo_v45  = csm_data.cosmo_daily_data(t_1_d, t_2_d, clm_name, parc_v45  , ts) 
    d_cosmo_v45e = csm_data.cosmo_daily_data(t_1_d, t_2_d, clm_name, parc_v45e , ts) 
    
    
    #Get Hyras data
    t2m_d  = flnt.daily_data(t_1_d, t_2_d, df_t2m_hyras['T_2M'] , ts, 'HYRAS' )
    tmax_d = flnt.daily_data(t_1_d, t_2_d, df_t2m_hyras['T_MAX'], ts, 'HYRAS' )
    tmin_d = flnt.daily_data(t_1_d, t_2_d, df_t2m_hyras['T_MIN'], ts, 'HYRAS' )
    ts_d   = flnt.daily_data(t_1_d, t_2_d, df_t2m_hyras['T_S']  , ts, 'HYRAS' )
    
        
    # Get climatic mean values for each day in June for GLEAM data
    gleam_Epa_d = flnt.daily_data(t_1_d, t_2_d, df_gleam['Ep_a'], ts, 'GLEAM')
    gleam_Eta_d = flnt.daily_data(t_1_d, t_2_d, df_gleam['Et_a'], ts, 'GLEAM')
    gleam_Epb_d = flnt.daily_data(t_1_d, t_2_d, df_gleam['Ep_b'], ts, 'GLEAM')
    gleam_Etb_d = flnt.daily_data(t_1_d, t_2_d, df_gleam['Et_b'], ts, 'GLEAM')
    

    if input_region == '1': 
        # Parc
        #flux_le_d     = flnt.daily_data(t_1_d, t_2_d, df_fluxnet['LE']     , ts, 'FL') 
        lh_d = flnt.daily_data(t_1_d, t_2_d, df_euronet['LE'], ts, 'EU')
        sh_d = flnt.daily_data(t_1_d, t_2_d, df_euronet['H'] , ts, 'EU')
    elif input_region == '2':
        # Linden
        lh_d = flnt.daily_data(t_1_d, t_2_d, df_in_situ['LatHeat'] , ts, 'Li')
        sh_d = flnt.daily_data(t_1_d, t_2_d, df_in_situ['SensHeat'], ts, 'Li') 
    else:
        # Lindenberg
        lh_d = flnt.daily_data(t_1_d, t_2_d, df_in_situ['LHFL_1'], ts, 'Lind')
        sh_d = flnt.daily_data(t_1_d, t_2_d, df_in_situ['SHFL_1'], ts, 'Lind')      
    
    
    # Create a new dataframe with GLEAM, FLUXNET and EURONET data
    df_obs_d = pd.concat([lh_d, sh_d, gleam_Epa_d, gleam_Eta_d, 
                                      gleam_Epb_d, gleam_Etb_d,
                                      t2m_d, tmax_d, tmin_d, ts_d], axis = 1)
    
    # Rename columnsin dataframe with observations
    df_obs_d.columns = ['LE', 'H', 'Ep_a', 'Et_a',
                                   'Ep_b', 'Et_b',
                                   'T_2M', 'TMAX', 'TMIN', 'TS' ]
    

    for i in range(len(clm_name)):
        plot_d = vsp.get_d(d_cosmo_orig, d_cosmo_v35, d_cosmo_v45, 
                           d_cosmo_v45e, df_obs_d   , clm_name[i],
                           name_2[i]   , data_exit  , y_min_d[i] , 
                           y_max_d[i]  , y_step_d[i], input_region)





elif mode == 3:
    #--------------------------------------------------------------------------
    # Get diurnal values
    #--------------------------------------------------------------------------
    t_1h = pd.to_datetime(['2010-06-01', '2011-06-01', '2012-06-01',
                           '2013-06-01', '2014-06-01', '2015-06-01'])
    t_2h = pd.to_datetime(['2010-08-31', '2011-08-31', '2012-08-31', 
                           '2013-08-31', '2014-08-31', '2015-08-31']) 
    
    t_1d = pd.to_datetime(['2010-06-01', '2011-06-01', '2012-06-01',
                           '2013-06-01', '2014-06-01', '2015-06-01'])
    t_2d = pd.to_datetime(['2010-08-31', '2011-08-31', '2012-08-31',
                           '2013-08-31', '2014-08-31', '2015-08-31'])                                
    
    
    # Get climatic mean values for each day in June for COSMO data
    h_cosmo_orig = csm_data.cosmo_hourly_data(t_1h, t_2h, clm_name, parc01_ctr) 
    h_cosmo_v35  = csm_data.cosmo_hourly_data(t_1h, t_2h, clm_name, parc_v35  ) 
    h_cosmo_v45  = csm_data.cosmo_hourly_data(t_1h, t_2h, clm_name, parc_v45  ) 
    h_cosmo_v45e = csm_data.cosmo_hourly_data(t_1h, t_2h, clm_name, parc_v45e ) 
    
    
    if input_region == '1':
        # Parc
        lh_h = flnt.hourly_data(t_1h, t_2h, df_fluxnet['LE']  ) 
        sh_h = flnt.hourly_data(t_1h, t_2h, df_euronet['H']   )
    elif input_region == '2':
        # Linden
        lh_h = flnt.hourly_data(t_1h, t_2h, df_in_situ['LatHeat'] )
        sh_h = flnt.hourly_data(t_1h, t_2h, df_in_situ['SensHeat'])        
    else:
        # Lindenberg
        lh_h = flnt.daily_data(t_1h, t_2h, df_in_situ['LHFL_1'])
        sh_h = flnt.daily_data(t_1h, t_2h, df_in_situ['SHFL_1'])          
    
    # Create a new dataframe with GLEAM, FLUXNET and EURONET data
    df_obs_h = pd.concat([lh_h, sh_h], axis = 1)
    
    # Rename columnsin dataframe with observations
    df_obs_h.columns = ['LE', 'H' ]
    
    
    
    gleam_Epa_h = flnt.daily_data(t_1d, t_2d, df_gleam['Ep_a'], ts, 'GLEAM').mean() / 12
    gleam_Epb_h = flnt.daily_data(t_1d, t_2d, df_gleam['Ep_b'], ts, 'GLEAM').mean() / 12
    
    pt_gleam_Epa = pd.Series([gleam_Epa_h], [12])
    pt_gleam_Epb = pd.Series([gleam_Epb_h], [12])
    
    
    df_point = pd.concat([pt_gleam_Epa, pt_gleam_Epb], axis = 1)
    
    df_point.columns = ['Ep_a', 'Ep_b']
 

    for i in range(len(clm_name)):
        plot_h = vsp.get_h(h_cosmo_orig, h_cosmo_v35, h_cosmo_v45, 
                           h_cosmo_v45e, df_obs_h   ,   df_point , clm_name[i],
                           name_2[i]   , data_exit  , y_min_h[i] , 
                           y_max_h[i]  , y_step_h[i], input_region)    
        


elif mode == 4:
    #--------------------------------------------------------------------------
    # Get verification plots
    #--------------------------------------------------------------------------
    
  
    t_1h = pd.to_datetime(['2011-07-05'])
    t_2h = pd.to_datetime(['2011-07-15']) 
    
    list_data = [] 
    for  tr in range(len(t_1h)):       
        period = pd.date_range(t_1h[tr], t_2h[tr], freq = '1H') 
        
        if input_region == '1':                                 
            lh_u = df_fluxnet['LE'][period]            
            sh_u = df_euronet['H'][period]
        elif input_region == '2':
            # Linden
            lh_u = df_in_situ['LatHeat'][period]
            sh_u = df_in_situ['SensHeat'][period]             
        else:
            # Lindenberg
            lh_u = df_in_situ['LHFL_1'][period]
            sh_u = df_in_situ['SHFL_1'][period]            
            
    
        # Create a new dataframe with GLEAM, FLUXNET and EURONET data
        df_obs_u = pd.concat([lh_u, sh_u], axis = 1)
    
        # Rename columnsin dataframe with observations
        df_obs_u.columns = ['LE', 'H']    
        
        
        time_step = None
        
        cosmo_orig = csm_data.get_timeseries(clm_name, parc01_ctr, period, time_step)
        cosmo_v35  = csm_data.get_timeseries(clm_name, parc_v35  , period, time_step)
        cosmo_v45  = csm_data.get_timeseries(clm_name, parc_v45  , period, time_step)
        cosmo_v45e = csm_data.get_timeseries(clm_name, parc_v45e , period, time_step)
    
    
        df_cosmo_o    = pd.concat(cosmo_orig, axis = 1)
        df_cosmo_v35  = pd.concat(cosmo_v35 , axis = 1)
        df_cosmo_v45  = pd.concat(cosmo_v45 , axis = 1)
        df_cosmo_v45e = pd.concat(cosmo_v45e, axis = 1)
     

        for i in range(len(clm_name)):
            plot_u = vsp.get_u(df_cosmo_o   , df_cosmo_v35, df_cosmo_v45, 
                               df_cosmo_v45e, df_obs_u    ,  clm_name[i],
                               name_2[i]    , data_exit   , y_min_u[i]  , 
                               y_max_u[i]   , y_step_u[i], input_region)


elif mode == 5:
    #--------------------------------------------------------------------------
    # Get heat waves 
    #--------------------------------------------------------------------------
    # Create time period
    #t_1_m = pd.to_datetime(['2010-01-01'])
    #t_2_m = pd.to_datetime(['2015-12-31'])
    t_1_m = pd.to_datetime(['2000-01-01'])
    t_2_m = pd.to_datetime(['2017-12-31'])
    period       = pd.date_range(t_1_m[0], t_2_m[0], freq = '1H') 
    
    time_step = '1M'
    
    data_cosmo = csm_data.get_timeseries(clm_name, parc01_ctr, period, time_step)             
    df_cosmo_orig = pd.concat(data_cosmo, axis = 1)
    
    
    t2m_mean = df_cosmo_orig['T_2M'].mean()
    t2m_std  = df_cosmo_orig['T_2M'].std()
    
    # Create a nan timeseries
    extrem = pd.Series(np.nan, index = df_cosmo_orig.index)
    super_hot = pd.Series(np.nan, index = df_cosmo_orig.index)
    super_col = pd.Series(np.nan, index = df_cosmo_orig.index)
    #test_ser = []
    for i in range(len(df_cosmo_orig['T_2M'])):
        extrem[i] = (df_cosmo_orig['T_2M'][i] - t2m_mean) / t2m_std
        
    
    for i in range(len(extrem)): 
        if extrem[i] > 1.45:
            super_hot[i] = extrem[i]           
        elif extrem[i] < -1.5:
            super_col[i] = extrem[i]         
        else:
            super_hot[i] = np.nan 
            super_col[i] = np.nan 
    
    name_plot = 'from 2000 to 2017'
    x_start   = '2000-01-01'
    x_stop    = '2017-12-31'
    
    
    verf_plot = vsp.plot_waves(extrem, super_hot, super_col, name_plot, domain,
                               station_plot, x_start, x_stop, data_exit)

elif mode == 6:          
    #--------------------------------------------------------------------------
    # Get summer values
    #--------------------------------------------------------------------------
    
    #t_1h = pd.to_datetime(['2010-06-01', '2011-06-01', '2012-06-01', '2013-06-01', '2014-06-01', '2015-06-01'])
    #t_2h = pd.to_datetime(['2010-08-31', '2011-08-31', '2012-08-31', '2013-08-31', '2014-08-31', '2015-08-31']) 
      
    t_1h = pd.to_datetime(['2010-07-01', '2011-07-01', '2012-07-01', 
                           '2013-07-01', '2014-06-01', '2015-06-01'])
    t_2h = pd.to_datetime(['2010-07-05', '2011-07-05', '2012-07-05',
                           '2013-07-05', '2014-07-05', '2015-07-05'])  
    
    
    list_data = [] 
    for  tr in range(len(t_1h)):       
        period = pd.date_range(t_1h[tr], t_2h[tr], freq = '1H')                                 
        d_data = df_fluxnet['LE'][period]  
        list_data.append(d_data)    
            
    # Concat all year in on dataframe
    data_d = pd.concat(list_data, axis = 1)    
    data_d.columns = ['LE_2010', 'LE_2011', 'LE_2012',
                      'LE_2013', 'LE_2014', 'LE_2015']
    
    data_d = data_d.resample('6H').mean()
    
    # Reset index
    data_ds = data_d.reset_index()
    
    
    
    d_id    = data_ds['index'].dt.year
    
    list_2010_id = []
    list_2011_id = []
    list_2012_id = []
    list_2013_id = []
    list_2014_id = []
    list_2015_id = []
    
    for i in range(len(d_id)):
        if d_id[i] == 2010:
            list_2010_id.append(d_id.index[i]) 
        elif d_id[i] == 2011:
            list_2011_id.append(d_id.index[i])
        elif d_id[i] == 2012:  
            list_2012_id.append(d_id.index[i])       
        elif d_id[i] == 2013:  
            list_2013_id.append(d_id.index[i])  
        elif d_id[i] == 2014:  
            list_2014_id.append(d_id.index[i])
        elif d_id[i] == 2015:  
            list_2015_id.append(d_id.index[i])  
        else:
            print ('No data')
    
    index_new = range(0, 2184, 1)
    
    ts_2010 = data_ds[list_2010_id[0]:list_2010_id[-1]]    
    ts_2010 = ts_2010.drop(['LE_2011','LE_2012','LE_2013', 'LE_2014', 'LE_2015'], axis=1)
    ts_2010 = ts_2010.reset_index()
    ts_2010 = ts_2010.drop(['level_0', 'index'], axis=1)
    
    ts_2011 = data_ds[list_2011_id[0]:list_2011_id[-1]]
    ts_2011 = ts_2011.drop(['LE_2010','LE_2012','LE_2013', 'LE_2014', 'LE_2015'], axis=1)
    ts_2011 = ts_2011.reset_index()
    ts_2011 = ts_2011.drop(['level_0', 'index'], axis=1)
    
    ts_2012 = data_ds[list_2012_id[0]:list_2012_id[-1]]    
    ts_2012 = ts_2012.drop(['LE_2010','LE_2011','LE_2013', 'LE_2014', 'LE_2015'], axis=1)
    ts_2012 = ts_2012.reset_index()
    ts_2012 = ts_2012.drop(['level_0', 'index'], axis=1)
    
    ts_2013 = data_ds[list_2013_id[0]:list_2013_id[-1]]    
    ts_2013 = ts_2013.drop(['LE_2010','LE_2011','LE_2012', 'LE_2014', 'LE_2015'], axis=1)
    ts_2013 = ts_2013.reset_index()
    ts_2013 = ts_2013.drop(['level_0', 'index'], axis=1)
    
    ts_2014 = data_ds[list_2014_id[0]:list_2014_id[-1]]    
    ts_2014 = ts_2014.drop(['LE_2010','LE_2011','LE_2012', 'LE_2013', 'LE_2015'], axis=1)
    ts_2014 = ts_2014.reset_index()
    ts_2014 = ts_2014.drop(['level_0', 'index'], axis=1)
    
    ts_2015 = data_ds[list_2015_id[0]:list_2015_id[-1]]    
    ts_2015 = ts_2015.drop(['LE_2010','LE_2011','LE_2012', 'LE_2013', 'LE_2014'], axis=1)
    ts_2015 = ts_2015.reset_index()
    ts_2015 = ts_2015.drop(['level_0'], axis=1)
     
    
    
    new_df = pd.concat([ts_2010, ts_2011, ts_2012,
                        ts_2013, ts_2014, ts_2015], axis = 1)  
    new_df_2 = new_df.set_index('index')
    
    new_df_3 = new_df_2.mean(axis = 1)
    
    
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)
    plt.plot(new_df_3.index ,  new_df_3, label = 'fluxnet'    , color = 'blue'  , linestyle = '-'  )
    plt.savefig(data_exit +'Test.png', format = 'png', dpi = 300)



    
elif mode == 7:
    #--------------------------------------------------------------------------
    # Statistic analysis
    #--------------------------------------------------------------------------  
    
    # Create time period
    t_1_m = pd.to_datetime(['2010-01-01'])
    t_2_m = pd.to_datetime(['2015-12-31'])
    
    period = pd.date_range(t_1_m[0]   , t_2_m[0], freq = '1H') 
    period_GL = pd.date_range(t_1_m[0], t_2_m[0], freq = '1D')
    
    time_step = '1D'
    
    data_cosmo_orig = csm_data.get_timeseries(clm_name, parc01_ctr, period, time_step)  
    data_cosmo_v35  = csm_data.get_timeseries(clm_name, parc_v35  , period, time_step)
    data_cosmo_v45  = csm_data.get_timeseries(clm_name, parc_v45  , period, time_step)
    data_cosmo_v45e = csm_data.get_timeseries(clm_name, parc_v45e , period, time_step)
    
    # Get COSMO data           
    df_cosmo_orig = pd.concat(data_cosmo_orig, axis = 1).interpolate()
    df_cosmo_v35  = pd.concat(data_cosmo_v35 , axis = 1).interpolate()
    df_cosmo_v45  = pd.concat(data_cosmo_v45 , axis = 1).interpolate()
    df_cosmo_v45e = pd.concat(data_cosmo_v45e, axis = 1).interpolate()
    
    #Get Hyras data
    t2m  = df_t2m_hyras['T_2M'][period_GL].resample(time_step).mean()
    tmax = df_t2m_hyras['T_MAX'][period_GL].resample(time_step).mean()
    tmin = df_t2m_hyras['T_MIN'][period_GL].resample(time_step).mean()
    ts   = df_t2m_hyras['T_S'][period_GL].resample(time_step).mean()
    
    # Get GLEAM data
    gl_Epa = df_gleam['Ep_a'][period_GL].resample(time_step).mean()  
    gl_Eta = df_gleam['Et_a'][period_GL].resample(time_step).mean()  
    gl_Epb = df_gleam['Ep_b'][period_GL].resample(time_step).mean()  
    gl_Etb = df_gleam['Et_b'][period_GL].resample(time_step).mean()  

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
              
    
    # Temperature statistic
    t2m_st_orig      = stat_tepm(df_cosmo_orig['T_2M']   , t2m   , 'COSMO_T2M'      )
    tmax_st_orig     = stat_tepm(df_cosmo_orig['TMAX_2M'], tmax  , 'COSMO_TMAX'     )
    tmin_st_orig     = stat_tepm(df_cosmo_orig['TMIN_2M'], tmin  , 'COSMO_TMIN'     )
    ts_st_orig       = stat_tepm(df_cosmo_orig['T_S']    , ts    , 'COSMO_TS'       )
    aevap_st_orig_a  = stat_tepm(df_cosmo_orig['AEVAP_S'], gl_Eta, 'COSMO_Epa'      )  # was gl_Epa
    aevap_st_orig_b  = stat_tepm(df_cosmo_orig['AEVAP_S'], gl_Etb, 'COSMO_Epb'      )  # was gl_Epb
    zverbo_st_orig_a = stat_tepm(df_cosmo_orig['ZVERBO'] , gl_Epa, 'COSMO_Eta'      )  # was gl_Eta
    zverbo_st_orig_b = stat_tepm(df_cosmo_orig['ZVERBO'] , gl_Epb, 'COSMO_Etb'      )  # was gl_Etb
    ashfl_st_orig    = stat_tepm(df_cosmo_orig['ASHFL_S'], sh_stat,'COSMO_ASHFL_FL' )
    alhfl_st_orig    = stat_tepm(df_cosmo_orig['ALHFL_S'], lh_stat,'COSMO_ALHFL_EU' )
    
    t2m_st_35        = stat_tepm(df_cosmo_v35['T_2M']    , t2m   , 'COSMO_v3.5_T2M'     )
    tmax_st_35       = stat_tepm(df_cosmo_v35['TMAX_2M'] , tmax  , 'COSMO_v3.5_TMAX'    )
    tmin_st_35       = stat_tepm(df_cosmo_v35['TMIN_2M'] , tmin  , 'COSMO_v3.5_TMIN'    )
    ts_st_35         = stat_tepm(df_cosmo_v35['T_S']     , ts    , 'COSMO_v3.5_TS'      )
    aevap_st_35_a    = stat_tepm(df_cosmo_v35['AEVAP_S'] , gl_Eta, 'COSMO_v3.5_Epa'     )
    aevap_st_35_b    = stat_tepm(df_cosmo_v35['AEVAP_S'] , gl_Etb, 'COSMO_v3.5_Epb'     )
    zverbo_st_35_a   = stat_tepm(df_cosmo_v35['ZVERBO']  , gl_Epa, 'COSMO_v3.5_Eta'     )
    zverbo_st_35_b   = stat_tepm(df_cosmo_v35['ZVERBO']  , gl_Epb, 'COSMO_v3.5_Etb'     )
    ashfl_st_35      = stat_tepm(df_cosmo_v35['ASHFL_S'] , sh_stat,'COSMO_v3.5_ASHFL_FL')
    alhfl_st_35      = stat_tepm(df_cosmo_v35['ALHFL_S'] , lh_stat,'COSMO_v3.5_ALHFL_FL')

    
    t2m_st_45       = stat_tepm(df_cosmo_v45['T_2M']    , t2m   , 'COSMO_v4.5_T2M'      )
    tmax_st_45      = stat_tepm(df_cosmo_v45['TMAX_2M'] , tmax  , 'COSMO_v4.5_TMAX'     )
    tmin_st_45      = stat_tepm(df_cosmo_v45['TMIN_2M'] , tmin  , 'COSMO_v4.5_TMIN'     )
    ts_st_45        = stat_tepm(df_cosmo_v45['T_S']     , ts    , 'COSMO_v4.5_TS'       )
    aevap_st_45_a   = stat_tepm(df_cosmo_v45['AEVAP_S'] , gl_Eta, 'COSMO_v4.5_Epa'      )
    aevap_st_45_b   = stat_tepm(df_cosmo_v45['AEVAP_S'] , gl_Etb, 'COSMO_v4.5_Epb'      )
    zverbo_st_45_a  = stat_tepm(df_cosmo_v45['ZVERBO']  , gl_Epa, 'COSMO_v4.5_Eta'      )
    zverbo_st_45_b  = stat_tepm(df_cosmo_v45['ZVERBO']  , gl_Epb, 'COSMO_v4.5_Etb'      )
    ashfl_st_45     = stat_tepm(df_cosmo_v45['ASHFL_S'] , sh_stat,'COSMO_v4.5_ASHFL_FL' )
    alhfl_st_45     = stat_tepm(df_cosmo_v45['ALHFL_S'] , lh_stat,'COSMO_v4.5_ALHFL_FL' )
    
    t2m_st_45e      = stat_tepm(df_cosmo_v45e['T_2M']   , t2m   , 'COSMO_v4.5e_T2M'     )
    tmax_st_45e     = stat_tepm(df_cosmo_v45e['TMAX_2M'], tmax  , 'COSMO_v4.5e_TMAX'    )
    tmin_st_45e     = stat_tepm(df_cosmo_v45e['TMIN_2M'], tmin  , 'COSMO_v4.5e_TMIN'    )
    ts_st_45e       = stat_tepm(df_cosmo_v45e['T_S']    , ts    , 'COSMO_v4.5e_TS'      )
    aevap_st_45e_a  = stat_tepm(df_cosmo_v45e['AEVAP_S'], gl_Eta, 'COSMO_v4.5e_Epa'     )
    aevap_st_45e_b  = stat_tepm(df_cosmo_v45e['AEVAP_S'], gl_Etb, 'COSMO_v4.5e_Epb'     )
    zverbo_st_45e_a = stat_tepm(df_cosmo_v45e['ZVERBO'] , gl_Epa, 'COSMO_45e_Eta'       )
    zverbo_st_45e_b = stat_tepm(df_cosmo_v45e['ZVERBO'] , gl_Epb, 'COSMO_45e_Etb'       )
    ashfl_st_45e    = stat_tepm(df_cosmo_v45e['ASHFL_S'], sh_stat,'COSMO_v4.5e_ASHFL_FL')
    alhfl_st_45e    = stat_tepm(df_cosmo_v45e['ALHFL_S'], lh_stat,'COSMO_v4.5e_ALHFL_FL')
    
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
    
    
    

    
    df_cosmo_stat_v35  = stat_cosmo(df_cosmo_orig, df_cosmo_v35)
    df_cosmo_stat_v45  = stat_cosmo(df_cosmo_orig, df_cosmo_v45)
    df_cosmo_stat_v45e = stat_cosmo(df_cosmo_orig, df_cosmo_v45e)
    
    df_stat_cosmo = pd.concat([df_cosmo_stat_v35, df_cosmo_stat_v45, df_cosmo_stat_v45e], axis = 0)
    df_stat_cosmo.to_excel(data_exit + 'COSMO_stat.xlsx', float_format='%.3f')
    
    

  
 











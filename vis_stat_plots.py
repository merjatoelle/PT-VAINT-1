# -*- coding: utf-8 -*-
"""
Created on Mon May 31 15:00:32 2021

@author: churiulin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




#------------------------------------------------------------------------------
# Subroutine: get_plot_m
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average montly values)
#
# 
# Input parameters : df     - data
#                    param  - name of columns   
#
#
# Output parameters: Plot with parameters
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.05.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_m(df, df2, df3, df4, df5, param, name_2, data_out, y1, y2, step, status):
    #print (status)
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)
    
    plt.plot(df.index ,  df[param]         , label = 'Cosmo_orig'    , color = 'blue'   , linestyle = '-'  )
    plt.plot(df2.index, df2[param]         , label = 'Cosmo_v3.5'    , color = 'orange' , linestyle = '--' )
    plt.plot(df3.index, df3[param]         , label = 'Cosmo_v4.5'    , color = 'green'  , linestyle = '-.', alpha = 0.4 )
    plt.plot(df4.index, df4[param]         , label = 'Cosmo_v4.5e'   , color = 'red'    , linestyle = ':' , alpha = 0.6 )    
    
    if param == 'ALHFL_S':
        plt.plot(df5.index, df5['LE'], label = 'OBS', color = 'cyan'  , alpha = 0.5)
    elif param == 'ASHFL_S': 
        plt.plot(df5.index, df5['H'] , label = 'OBS', color = 'violet', alpha = 0.5)            
    elif param == 'AEVAP_S':
        plt.plot(df5.index, df5['Et_a'], label = 'Gleam_v3.5a', color = 'magenta'  , alpha = 0.5) # was Ep_a
        plt.plot(df5.index, df5['Et_b'], label = 'Gleam_v3.5b', color = 'lime'     , alpha = 0.5) # was Ep_b   
    elif param == 'ZVERBO':
        plt.plot(df5.index, df5['Ep_a'], label = 'Gleam_v3.5a', color = 'magenta'  , alpha = 0.5) # was Et_a
        plt.plot(df5.index, df5['Ep_b'], label = 'Gleam_v3.5b', color = 'lime'     , alpha = 0.5) # was Et_b      
    elif param == 'T_2M': 
        plt.plot(df5.index, df5['T_2M'], label = 'obs', color = 'purple', alpha = 0.5)
    elif param == 'T_S': 
        plt.plot(df5.index, df5['TS']  , label = 'obs', color = 'purple', alpha = 0.5)
    elif param == 'TMAX_2M': 
        plt.plot(df5.index, df5['TMAX'], label = 'obs', color = 'purple', alpha = 0.5)
    elif param == 'TMIN_2M': 
        plt.plot(df5.index, df5['TMIN'], label = 'obs', color = 'purple', alpha = 0.5)  
    else:
        print('no additional parameters')    
        
    ax.legend()
    
    if status == '1':
        ax.set_title('Annual cycle of ' + param + ' from 2010 to 2015' + 
                     '\n\n' + 'Domain: Parc' + '     ' + 'Station: Rollesbroich',
                     color = 'black', fontsize = 14, pad = 20) 

    elif status == '2':    
        ax.set_title('Annual cycle of ' + param + ' from 2010 to 2015' + 
                     '\n\n' + 'Domain: Linden'    + '     ' + 'Station: Linden',
                     color = 'black', fontsize = 14, pad = 20)    
    elif status == '3':
        ax.set_title('Annual cycle of ' + param + ' from 2010 to 2015' + 
                     '\n\n' + 'Domain: Lindenberg' + '     ' + 'Station: Lindenberg',
                     color = 'black', fontsize = 14, pad = 20)    
    else:
        print('nnnn')
        
    ax.set_ylabel(name_2, color = 'black', fontsize = 14, labelpad = 20)

    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    
    plt.grid()
    
    plt.savefig(data_out + 'Annual/' +param + '_annual.png', format = 'png', dpi = 300)

    plt.close(fig)        
    plt.gcf().clear() 
    
 
  
#------------------------------------------------------------------------------
# Subroutine: get_plot_d
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
#
# 
# Input parameters : df     - data
#                    param  - name of columns   
#
#
# Output parameters: Plot with parameters
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.05.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_d(df, df2, df3, df4, df5, param, name_2, data_out, y1, y2, step, input_region):
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    
    plt.plot(df.index ,  df[param], label = 'Cosmo_orig' , color = 'blue'  , linestyle = '-'  )
    plt.plot(df2.index, df2[param], label = 'Cosmo_v3.5' , color = 'orange', linestyle = '--' )
    plt.plot(df3.index, df3[param], label = 'Cosmo_v4.5' , color = 'green' , linestyle = '-.', alpha = 0.4 )
    plt.plot(df4.index, df4[param], label = 'Cosmo_v4.5e', color = 'red'   , linestyle = ':' , alpha = 0.6 )

    if param == 'ALHFL_S':
        plt.plot(df5.index, df5['LE'], label = 'OBS', color = 'cyan', alpha = 0.5)
    elif param == 'ASHFL_S': 
        plt.plot(df5.index, df5['H'] , label = 'OBS', color = 'cyan', alpha = 0.5)            
    elif param == 'AEVAP_S':
        plt.plot(df5.index, df5['Et_a'], label = 'Gleam_v3.5a', color = 'magenta'  , alpha = 0.5)
        plt.plot(df5.index, df5['Et_b'], label = 'Gleam_v3.5b', color = 'lime'     , alpha = 0.5)    
    elif param == 'ZVERBO':
        plt.plot(df5.index, df5['Ep_a'], label = 'Gleam_v3.5a', color = 'magenta'  , alpha = 0.5)
        plt.plot(df5.index, df5['Ep_b'], label = 'Gleam_v3.5b', color = 'lime'     , alpha = 0.5)       
    elif param == 'T_2M': 
        plt.plot(df5.index, df5['T_2M'], label = 'OBS', color = 'purple', alpha = 0.5)
    elif param == 'T_S': 
        plt.plot(df5.index, df5['TS']  , label = 'OBS', color = 'purple', alpha = 0.5)
    elif param == 'TMAX_2M': 
        plt.plot(df5.index, df5['TMAX'], label = 'OBS', color = 'purple', alpha = 0.5)
    elif param == 'TMIN_2M': 
        plt.plot(df5.index, df5['TMIN'], label = 'OBS', color = 'purple', alpha = 0.5)        
    
    ax.legend()

    if input_region == '1':
        ax.set_title('Daily average values of ' + param + ' in June from 2010 to 2015' +
                     '\n\n' + 'Domain: Parc' + '     ' + 'Station: Rollesbroich',
                     color = 'black', fontsize = 14, pad = 20) 

    elif input_region == '2':    
        ax.set_title('Daily average values of ' + param + ' in June from 2010 to 2015' +
                     '\n\n' + 'Domain: Linden'  + '     ' + 'Station: Linden',
                     color = 'black', fontsize = 14, pad = 20)    
    else:
        ax.set_title('Daily average values of ' + param + ' in June from 2010 to 2015' +
                     '\n\n' + 'Domain: Lindenberg' + '     ' + 'Station: Lindenberg',
                     color = 'black', fontsize = 14, pad = 20)    
    
    ax.set_xlabel('Day of month', color = 'black', fontsize = 14, labelpad = 20)
    ax.set_ylabel(name_2, color = 'black', fontsize = 14, labelpad = 20)

    ax.get_xticks()
    ax.set_xticks(np.arange(0, 30.1, 5))
    
    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    
    plt.grid()
    
    plt.savefig(data_out + 'Monthly/' + param + '_June.png', format = 'png', dpi = 300)
    
    plt.close(fig)        
    plt.gcf().clear() 
#------------------------------------------------------------------------------












#------------------------------------------------------------------------------
# Subroutine: get_plot_h
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
#
# 
# Input parameters : df     - data
#                    param  - name of columns   
#
#
# Output parameters: Plot with parameters
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.05.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_h(df, df2, df3, df4, df5, df6, param, name_2, data_out, y1, y2, step, input_region):
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    plt.plot(df.index ,  df[param], label = 'Cosmo_orig' , color = 'blue'  , linestyle = '-'  )
    plt.plot(df2.index, df2[param], label = 'Cosmo_v3.5' , color = 'orange', linestyle = '--' )
    plt.plot(df3.index, df3[param], label = 'Cosmo_v4.5' , color = 'green' , linestyle = '-.', alpha = 0.4 )
    plt.plot(df4.index, df4[param], label = 'Cosmo_v4.5e', color = 'red'   , linestyle = ':' , alpha = 0.6 )

    if param == 'ALHFL_S':
        plt.plot(df5.index, df5['LE'], label = 'OBS', color = 'cyan' , alpha = 0.5)
    elif param == 'ASHFL_S': 
        plt.plot(df5.index, df5['H'] , label = 'OBS', color = 'cyan' , alpha = 0.5)
        
    elif param == 'AEVAP_S':
        plt.scatter(df6.index, df6['Ep_a']     , label = 'Gleam_v3.5a'   , color = 'magenta', alpha = 0.5)
        plt.scatter(df6.index, df6['Ep_b']     , label = 'Gleam_v3.5b'   , color = 'lime'   , alpha = 0.5)    
    #elif param == 'ZVERBO':
    #    plt.plot(df.index ,  df[param]         , label = 'Cosmo_orig'    , color = 'blue'   , linestyle = '-'  )
    #    plt.plot(df2.index, df2[param]         , label = 'Cosmo_v3.5'    , color = 'orange' , linestyle = '--' )
    #    plt.plot(df3.index, df3[param]         , label = 'Cosmo_v4.5'    , color = 'green'  , linestyle = '-.', alpha = 0.4 )
    #    plt.plot(df4.index, df4[param]         , label = 'Cosmo_v4.5e'   , color = 'red'    , linestyle = ':' , alpha = 0.6 )
    #    plt.scatter(df6.index, df6['Et_a']     , label = 'Gleam_v3.5a'   , color = 'magenta', alpha = 0.5)
    #    plt.scatter(df6.index, df6['Et_b']     , label = 'Gleam_v3.5b'   , color = 'lime'   , alpha = 0.5)       
   
    ax.legend()
    
    if input_region == '1':
        ax.set_title('Diurnal cycle of ' + param + ' from June to August' +'\n\n'
                     + 'Domain: Parc' + '     ' + 'Station: Rollesbroich',
                     color = 'black', fontsize = 14, pad = 20)
    elif input_region == '2': 
        ax.set_title('Diurnal values of ' + param + ' from June to August' +'\n\n'
                     + 'Domain: Linden' + '     ' + 'Station: Linden',
                     color = 'black', fontsize = 14, pad = 20)
    else:
        ax.set_title('Diurnal cycle of ' + param + ' from June to August' +'\n\n'
                     + 'Domain: Lindenberg' + '     ' + 'Station: Lindenberg',
                     color = 'black', fontsize = 14, pad = 20)
    
    ax.set_xlabel('Hour', color = 'black', fontsize = 14, labelpad = 20)
    ax.set_ylabel(name_2, color = 'black', fontsize = 14, labelpad = 20)
 
    ax.get_xticks()
    ax.set_xticks(np.arange(0, 24.1, 3))
    
    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    
    plt.grid()
    
    plt.savefig(data_out +'Diurnal/' + param + '_Hour.png', format = 'png', dpi = 300)
    plt.close(fig)        
    plt.gcf().clear() 
#------------------------------------------------------------------------------
















#------------------------------------------------------------------------------
# Subroutine: get_plot_u
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
#
# 
# Input parameters : df     - data
#                    param  - name of columns   
#
#
# Output parameters: Plot with parameters
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 25.05.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_u(df, df2, df3, df4, df5, param, name_2, data_out, y1, y2, step, input_region):
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)
        
    plt.plot(df.index ,  df[param]   , label = 'Cosmo_orig' , color = 'blue'  , linestyle = '-'  )
    plt.plot(df2.index, df2[param]   , label = 'Cosmo_v3.5' , color = 'orange', linestyle = '--' )
    plt.plot(df3.index, df3[param]   , label = 'Cosmo_v4.5' , color = 'green' , linestyle = '-.', alpha = 0.4 )
    plt.plot(df4.index, df4[param]   , label = 'Cosmo_v4.5e', color = 'red'   , linestyle = ':' , alpha = 0.6 )
    
    if param == 'ALHFL_S':
        plt.plot(df5.index, df5['LE'], label = 'OBS', color = 'cyan', alpha = 0.5)
    elif param == 'ASHFL_S': 
        plt.plot(df5.index, df5['H'] , label = 'OBS', color = 'cyan', alpha = 0.5)            
    #elif param == 'AEVAP_S':
    #    plt.plot(df.index ,  df[param]         , label = 'Cosmo_orig'    , color = 'blue'   , linestyle = '-'  )
    #    plt.plot(df2.index, df2[param]         , label = 'Cosmo_v3.5'    , color = 'orange' , linestyle = '--' )
    #    plt.plot(df3.index, df3[param]         , label = 'Cosmo_v4.5'    , color = 'green'  , linestyle = '-.', alpha = 0.4 )
    #    plt.plot(df4.index, df4[param]         , label = 'Cosmo_v4.5e'   , color = 'red'    , linestyle = ':' , alpha = 0.6 )
    #    plt.scatter(df6.index, df6['Ep_a']     , label = 'Gleam_v3.5a'   , color = 'magenta', alpha = 0.5)
    #    plt.scatter(df6.index, df6['Ep_b']     , label = 'Gleam_v3.5b'   , color = 'lime'   , alpha = 0.5)    
    #elif param == 'ZVERBO':
    #    plt.plot(df.index ,  df[param]         , label = 'Cosmo_orig'    , color = 'blue'   , linestyle = '-'  )
    #    plt.plot(df2.index, df2[param]         , label = 'Cosmo_v3.5'    , color = 'orange' , linestyle = '--' )
    #    plt.plot(df3.index, df3[param]         , label = 'Cosmo_v4.5'    , color = 'green'  , linestyle = '-.', alpha = 0.4 )
    #    plt.plot(df4.index, df4[param]         , label = 'Cosmo_v4.5e'   , color = 'red'    , linestyle = ':' , alpha = 0.6 )
    #    plt.scatter(df6.index, df6['Et_a']     , label = 'Gleam_v3.5a'   , color = 'magenta', alpha = 0.5)
    #    plt.scatter(df6.index, df6['Et_b']     , label = 'Gleam_v3.5b'   , color = 'lime'   , alpha = 0.5)       
            
    ax.legend()

    time_period = ' from 05.07.2011 to 15.07.2011' + '\n\n'
    
    if input_region == '1':    
        ax.set_title('Hourly values of ' + param + time_period +
                     'Domain: Parc' + '     ' + 'Station: Rollesbroich',
                     color = 'black', fontsize = 14, pad = 20)
    elif input_region == '2':
        ax.set_title('Hourly values of ' + param + time_period +
                     'Domain: Linden' + '     ' + 'Station: Linden',
                     color = 'black', fontsize = 14, pad = 20) 
    else:
        ax.set_title('Hourly values of ' + param + time_period +
                     'Domain: Lindenberg' + '     ' + 'Station: Lindenberg',
                     color = 'black', fontsize = 14, pad = 20)
    
    
    ax.set_xlabel('Date', color = 'black', fontsize = 14, labelpad = 20)
    ax.set_ylabel(name_2, color = 'black', fontsize = 14, labelpad = 20)
    
    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    
    plt.grid()
    
    plt.savefig(data_out + 'Weekly/' + param + '_verif.png', format = 'png', dpi = 300)
    plt.close(fig)        
    plt.gcf().clear() 
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine: plot_waves
#------------------------------------------------------------------------------
#
# The subroutine needs for getting plot with information about heat and cold waves
#
# 
# Input parameters : ts_main     - data
#                    ts_hot  - name of columns   
#                    ts_cold
#                    interval
#                    domain
#                    station
#                    x_start
#                    x_stop
#                    data_exit
#
#
#
#
# Output parameters: Plot with T2M
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 01.06.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------





def plot_waves(ts_main, ts_hot, ts_cold, interval, domain, station, x_start, 
               x_stop, data_exit ):

    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    plt.plot(ts_main.index   ,  ts_main, label = 'T2_M'     , color = 'blue'  , linestyle = '-')
    plt.scatter(ts_hot.index ,  ts_hot , label = 'hot wave' , color = 'red'   , linewidths = 2 )
    plt.scatter(ts_cold.index,  ts_cold, label = 'cold wave', color = 'orange', linewidths = 2 )

    ax.legend(loc = 'lower right', frameon=True)
    
    ax.set_title('Heat and cold waves ' + interval + 
                 '\n\n' + 'Domain: '    + domain   + '     ' + 'Station: ' + station,
                 color = 'black', fontsize = 14, pad = 20)    

    ax.set_ylabel('Standart deviation', color = 'black', fontsize = 14, labelpad = 20)
    ax.set_xlabel('Years'             , color = 'black', fontsize = 14, labelpad = 20)

    ax.get_xticks()
    ax.set_xticks(pd.date_range(x_start, x_stop, freq = 'YS'))

    ax.get_yticks()
    ax.set_yticks(np.arange(-2.5, 2.51, 0.5))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
            
    plt.grid()
      
    plt.savefig(data_exit + 'Waves_' + interval +'.png', format = 'png', dpi = 300) 
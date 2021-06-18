# -*- coding: utf-8 -*-
"""
Created on Fri May 21 15:31:21 2021

@author: churiulin
"""

import math
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt





#------------------------------------------------------------------------------
# Subroutine: get_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual COSMO data
#
# 
# Input parameters : path     - path for data
#                    par_name - name of columns   
#
#
# Output parameters: df_euronet - the data frame with information about EURONET data
# 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 24.03.2021
#
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------


def get_data(path, par_name):
    df = pd.read_csv(path, skiprows = 0, sep=' ', skipinitialspace = True, 
                     header = None, parse_dates = {'Date':[0,1]}, index_col = 0,
                     na_values = ['9990','********','***','******'])
    df.columns = [par_name]  
 
    return df

#------------------------------------------------------------------------------


def montly_data(df_data):
    # reset index
    df_par  = df_data.reset_index()
    # Get number of months for each element
    num_id  = df_par['Date'].dt.month
    df_mean = df_par.groupby(num_id).mean()
    # Re-indexing
    time_index = pd.date_range('1/1/2019', '12/1/2019', freq='MS').strftime('%B')
    df_mean.index  = time_index    
    return df_mean


def daily_data(t_1, t_2, version, data):    
    list_data      = []  
    list_par_june  = []    
    for  tr in range(len(t_1)):  
        for i in range(len(version)):     
            # Get a time period
            period  = pd.date_range(t_1[tr], t_2[tr], freq = 'D')          
            df_data = data[version[i]][period]        
            # Add values to lists
            list_data.append(df_data)
    
    # Get one dataframe for parameters in June
    par_june = pd.concat(list_data , axis = 1)    
    # Reset index
    par_june = par_june.reset_index()
    # Get day index in June 
    day_id   = par_june['index'].dt.day
    
    for i in range(len((version))):
        par_june_mean = par_june[version[i]].groupby(day_id).mean()
        par_june_mean = par_june_mean.mean(axis = 1)
        par_june_mean = par_june_mean.rename(version[i])      
        list_par_june.append(par_june_mean)
    # Get data    
    par_d = pd.concat(list_par_june , axis = 1)
    return par_d

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

def get_plot_m(df, param):
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)
    
    plt.plot(df.index, df['HYRAS']     , label = 'HYRAS'      , color = 'purple')
    plt.plot(df.index, df['COSMO_ORIG'], label = 'Cosmo_orig' , color = 'blue'  )
    plt.plot(df.index, df['COSMO_35']  , label = 'Cosmo_v3.5' , color = 'orange')
    plt.plot(df.index, df['COSMO_45']  , label = 'Cosmo_v4.5' , color = 'green' )
    plt.plot(df.index, df['COSMO_45e'] , label = 'Cosmo_v4.5e', color = 'red'   )
            
    ax.legend()
    
    ax.set_title('Monthly average ' + param + ' from 2010 to 2015' +'\n\n' + 'domain: Parc', color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(param + ', C', color = 'black', fontsize = 14, labelpad = 20)


    ax.get_yticks()
    ax.set_yticks(np.arange(0, 25.1, 5))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    
    plt.grid()
    
    plt.savefig(data_out + param + '_annual.png', format = 'png', dpi = 300)


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


def get_plot_d(df, param):
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)
    
    plt.plot(df.index, df['HYRAS']     , label = 'HYRAS'      , color = 'purple')
    plt.plot(df.index, df['COSMO_ORIG'], label = 'Cosmo_orig' , color = 'blue'  )
    plt.plot(df.index, df['COSMO_35']  , label = 'Cosmo_v3.5' , color = 'orange')
    plt.plot(df.index, df['COSMO_45']  , label = 'Cosmo_v4.5' , color = 'green' )
    plt.plot(df.index, df['COSMO_45e'] , label = 'Cosmo_v4.5e', color = 'red'   )
            
    ax.legend()
    
    ax.set_title('Daily average values of ' + param + ' in June from 2010 to 2015' +'\n\n'
                 + 'domain: Parc' + '     ' + 'Station: Rollesbroich',
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(param + ', C', color = 'black', fontsize = 14, labelpad = 20)


    ax.get_xticks()
    ax.set_xticks(np.arange(0, 30.1, 5))
    
    ax.get_yticks()
    ax.set_yticks(np.arange(0, 25.1, 5))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    
    plt.grid()
    
    plt.savefig(data_out + param + '_June.png', format = 'png', dpi = 300)

#------------------------------------------------------------------------------






#------------------------------------------------------------------------------
# Main programm
#------------------------------------------------------------------------------

# Path to the main project folder
mf_com       = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'

# Path to subfolder
sf_statistic = 'ANALYSIS/HYRAS/PARC/'

# Types of data for analysis
version = ['HYRAS', 'COSMO_ORIG', 'COSMO_35', 'COSMO_45', 'COSMO_45e']
domain  = 'parc_domain'

# Types of parameters for analysis
parameters = ['T_2M', 'T_MAX', 'T_MIN', 'T_S']


#------------------------------------------------------------------------------
# Change if you know what are you doing
#------------------------------------------------------------------------------


t2m_list  = []
tmax_list = []
tmin_list = []
ts_list   = []

for i in range(len(parameters)):  
    for j in range(len(version)):           
        
        # Input data (main path to folders)
        data_in = mf_com + sf_statistic 
        data_out = mf_com + 'ANALYSIS/PLOTS/'
        
        # Input file name

        fn_in = version[j] + '_' + parameters[i] + '_mean_' + domain + '.csv'        
     
        
        # Input path + file name       
        path_in = data_in + fn_in    
        
        if parameters[i] == 'T_2M':
            df = get_data(path_in,  version[j])
            t2m_list.append(df)              
        elif parameters[i] == 'T_MAX':
            df = get_data(path_in,  version[j])
            tmax_list.append(df)
        elif parameters[i] == 'T_MIN':
            df = get_data(path_in,  version[j])
            tmin_list.append(df)
        elif parameters[i] == 'T_S':
            df = get_data(path_in,  version[j])
            ts_list.append(df)
        else:
            print ('Parameters are npt in list')


# Create dataframes for our parameters            
df_t2m  = pd.concat(t2m_list , axis = 1)
df_tmax = pd.concat(tmax_list, axis = 1)
df_tmin = pd.concat(tmin_list, axis = 1)
df_ts   = pd.concat(ts_list  , axis = 1)

#------------------------------------------------------------------------------
# Get average monhtly values (climatic)
#------------------------------------------------------------------------------

t2m_m  = montly_data(df_t2m)
tmax_m = montly_data(df_tmax)
tmin_m = montly_data(df_tmin)
ts_m   = montly_data(df_ts)

t2m_plot  = get_plot_m(t2m_m , 'T_2M' ) 
tmax_plot = get_plot_m(tmax_m, 'T_MAX')
tmin_plot = get_plot_m(tmin_m, 'T_MIN')
ts_plot   = get_plot_m(ts_m  , 'T_S'  )
 
#------------------------------------------------------------------------------    


#------------------------------------------------------------------------------
# Get avarage daily values (climatic)
#------------------------------------------------------------------------------

t_1 = pd.to_datetime(['2010-06-01', '2011-06-01', '2012-06-01', '2013-06-01', '2014-06-01', '2015-06-01'])
t_2 = pd.to_datetime(['2010-06-30', '2011-06-30', '2012-06-30', '2013-06-30', '2014-06-30', '2015-06-30'])                                

t2m_d  = daily_data(t_1, t_2, version, df_t2m)
tmax_d = daily_data(t_1, t_2, version, df_t2m)
tmin_d = daily_data(t_1, t_2, version, df_t2m)
ts_d   = daily_data(t_1, t_2, version, df_t2m)

t2m_d_plot  = get_plot_d(t2m_d , 'T_2M'  )
tmax_d_plot = get_plot_d(tmax_d, 'T_MAX' )
tmin_d_plot = get_plot_d(tmin_d, 'T_MIN' )
ts_d_plot   = get_plot_d(ts_d  , 'T_S'   )



    
    
    
    
    
    
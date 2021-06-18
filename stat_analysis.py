# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:32:43 2021

@author: churiulin
"""


import numpy as np
import pandas as pd

import KGE_RMSD   as kge 
import DAV_metric as dav 

from taylorDiagram import TaylorDiagram
import matplotlib.pyplot as plt


#------------------------------------------------------------------------------
# Section: Can be changed by user
#------------------------------------------------------------------------------ 

# The main path for folder with data
#mf_com = 'C:/Users/Churiulin/Desktop/STAT/'
          #'C:/Users/Churiulin/Desktop/COSMO_RESULTS/'
#mf_com = 'C:/Users/Churiulin/Desktop/STAT2/'

def statistic(main_path, sf_statistic, sssf_region, refer, ds_name):
    
    #--------------------------------------------------------------------------
    # Section 0: Define local statistical paths and parameters
    #--------------------------------------------------------------------------
    
    # Parameter list
    par_list = ['T_2M', 'T_MAX', 'T_MIN', 'T_S']
    
    df_stat_list = []
    for i in range(len(par_list)):
        # Main path
        mf_com = main_path

        # Path for statistic results and Tailor diagramm
        path_exit = mf_com + sf_statistic + refer + '/' + sssf_region    

        # Paths for subfolders for KGE and RMSD data
        sf_data_ref = sf_statistic + refer + '/' + sssf_region + refer   + '/'                   # The subfolder for refer data (observation)
        sf_data_ds  = sf_statistic + refer + '/' + sssf_region + ds_name + '/'                   # The subfolder for model data

        # Subfolders for DAV data
        sf_obs_data = sf_statistic + refer + '/' + sssf_region + refer   + '/'                   # The subfolder with HYRAS data    
        sf_lr_data  = sf_statistic + refer + '/' + sssf_region + 'COSMO_ORIG/'                   # The subfolder with lr data set - COSMO original
        sf_hr_data  = sf_statistic + refer + '/' + sssf_region + ds_name + '/'                   # The subfolder with hr data set - COSMO 3.5, 4.5, 4.5e 

 

        print (par_list[i])

        #--------------------------------------------------------------------------
        # Section 1: Run KGE and RMSD statistic analysis
        #--------------------------------------------------------------------------
    
        kge_res, rmsd_res, cor_res =  kge.KGE_RMSD_analysis(mf_com, sf_data_ref,
                                                            sf_data_ds, par_list[i],
                                                            refer, ds_name)


        #------------------------------------------------------------------------------
        # Section 2: Run DAV statistic analysis
        #------------------------------------------------------------------------------
    
        dav_res = dav.DAV_analysis(mf_com, sf_obs_data, 
                                           sf_lr_data ,
                                           sf_hr_data  ,
                                           par_list[i], refer, ds_name)
    
        #--------------------------------------------------------------------------
        # Section 3: Import results to excel
        #--------------------------------------------------------------------------
        
              
        STAT_result ={'Unit' : par_list[i], 'KGE' : kge_res, 'RMSD' : rmsd_res, 'CORR' : cor_res, 'DAV' : dav_res}
    
    
        df_stat = pd.DataFrame(list(STAT_result.items()), columns = ['Parameter','Values'])
        #df_stat.to_excel(path_exit + 'Statistic_' + par_list[i] + '_' + ds_name + '.xlsx',  float_format='%.3f')
        
        
        df_stat_list.append(df_stat)
    
    
 
    df_statistic = pd.concat(df_stat_list, axis = 1)
 
    df_statistic.to_excel(path_exit + 'Statistic_' + ds_name + '.xlsx',  float_format='%.3f')
        #df_stat.to_excel(path_exit + 'Statistic_' + par_list[i] + '_' + ds_name + '.xlsx',  float_format='%.3f')

    #------------------------------------------------------------------------------
    # Section 4: Plot Taylor diagram based on Yannick Copin example
    #------------------------------------------------------------------------------
    
    """
    Example of use of TaylorDiagram. Illustration dataset courtesy of Michael
    Rawlins.
    Rawlins, M. A., R. S. Bradley, H. F. Diaz, 2012. Assessment of regional climate
    model simulation estimates over the Northeast United States, Journal of
    Geophysical Research (2012JGRD..11723112R).
    """
    
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
        
        dia = TaylorDiagram(stdrefs[season], fig = fig, rect = rects[season],
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
    """
    
    return df_stat
    





























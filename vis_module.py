# -*- coding: utf-8 -*-
"""
The vis_module is the main program for data visualization of PT VAINT.

The progam contains subroutines:
    
    # Section for plots based on timesteps with mothly, yearly and next time intervals
    plot_2  ---> Option for 2 lines in a single plot
    plot_3  ---> Option for 3 lines in a single plot
    plot_4  ---> Option for 4 lines in a single plot
    plot_5  ---> Option for 5 lines in a single plot
    plot_6  ---> Option for 6 lines in a single plot
    plot_7  ---> Option for 7 lines in a single plot

    # Section for plots based on timesteps with hourly and daily time intervals
    plot_2d ---> Option for 2 lines in a single plot
    plot_3d ---> Option for 3 lines in a single plot
    plot_4d ---> Option for 4 lines in a single plot
    plot_5d ---> Option for 5 lines in a single plot
    plot_6d ---> Option for 6 lines in a single plot
    
    # Section for plots based on mean (climatic) values
    get_m      ---> annual cycly
    get_d      ---> daily cycle
    get_h      ---> diurnal cycle
    get_u      ---> user time interval (for example 1 week)
    plot_waves ---> heat and cold waves visualization
    
    # Section for Taylor diagram
    
    Taylor diagram 

Autors of project: Evgenii Churiulin, Merja Tölle, Center for Enviromental System
                                                   Research (CESR) 

                                                   
Acknowledgements: Vladimir Kopeikin, Denis Blinov, Yannick Copin


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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker


# Additional parameters for X and Y axis for plots
#------------------------------------------------------------------------------
# Plot 2
minorLocator_1   = AutoMinorLocator (n=5)
minorFormatter_1 = FormatStrFormatter('%.1f')

# Plot 3
minorLocator_2   = AutoMinorLocator (n=5)
minorFormatter_2 = FormatStrFormatter('%.1f')

#Plot 4
minorLocator_3   = AutoMinorLocator (n=4)
minorFormatter_3 = FormatStrFormatter('%.1f')

# Plot 5
minorLocator_4   = AutoMinorLocator (n=5)
minorFormatter_4 = FormatStrFormatter('%.1f')

# Plot 6
minorLocator_5   = AutoMinorLocator (n=5)
minorFormatter_5 = FormatStrFormatter('%.1f')

# Plot 2d
minorLocator_6   = AutoMinorLocator (n=5)
minorFormatter_6 = FormatStrFormatter('%.1f')

# Plot 3d
minorLocator_7   = AutoMinorLocator (n=4)
minorFormatter_7 = FormatStrFormatter('%.1f')

# Plot 4d
minorLocator_8   = AutoMinorLocator (n=5)
minorFormatter_8 = FormatStrFormatter('%.1f')

# Plot 5d
minorLocator_9   = AutoMinorLocator (n=5)
minorFormatter_9 = FormatStrFormatter('%.1f')

#Plot 6d
minorLocator_10   = AutoMinorLocator (n=5)
minorFormatter_10 = FormatStrFormatter('%.1f')


years = mdates.YearLocator() #every year
days = mdates.DayLocator(15)
yearFmt = mdates.DateFormatter('%Y')
#End section
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# plot_2
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 2 lines in a single plot 
#
# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                                       dapa plot (timeseries have to have a time
#                                       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    na_3, na4        - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------
def plot_2(ax, prr_1, prr_2,
               leg_1, leg_2, 
               na_3, na_4, date_ind, nst, l_p, 
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 

    ax.plot(prr_1.index, prr_1, label = leg_1 , color = 'tab:blue'  , 
                                                    linestyle = '-' )   
    ax.plot(prr_2.index, prr_2, label = leg_2 , color = 'tab:orange', 
                                                    linestyle = '--')   
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon = False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis ='y'  , which = 'major', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    ax.tick_params(axis ='y'  , which ='minor' , bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_1)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

# end def plot_2
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# plot_3
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 3 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3              dapa plot (timeseries have to have a time
#                                       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3       
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------       
def plot_3(ax, prr_1, prr_2, prr_3, 
               leg_1, leg_2, leg_3,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'tab:blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'tab:orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'tab:green' , linestyle = '-.')
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind,
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis ='y'  , which ='major', bottom    = True, top = False,
                   left = True, right = True  , labelleft ='on' , labelright = 'on')
    ax.tick_params(axis ='y'  , which ='minor', bottom    = True, top = False,
                   left = True, right = True  , labelleft ='on' , labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_2)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True,  which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)

# end def plot_3
#------------------------------------------------------------------------------
    

#------------------------------------------------------------------------------
# plot_4
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 4 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                                       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4       
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------
def plot_4(ax, prr_1, prr_2, prr_3, prr_4,
               leg_1, leg_2, leg_3, leg_4,
               na_3, na_4, date_ind, nst, l_p, 
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue' , linestyle = '-')
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'green', linestyle = '-')
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'brown', linestyle = '-') 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'  , linestyle = '-')
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_3)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)

# end def plot_4
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# plot_5
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 5 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                    prr_5              index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4      
#                    leg_5 
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------   
def plot_5(ax, prr_1, prr_2, prr_3, prr_4, prr_5, 
               leg_1, leg_2, leg_3, leg_4, leg_5,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'green' , linestyle = '-' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'brown' , linestyle = '-' ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = '-' )
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'black' , linestyle = '-.')
   
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_4)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)
    
# end def plot_5
#------------------------------------------------------------------------------ 
    
#------------------------------------------------------------------------------
# plot_6
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 6 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                    prr_5, prr_6       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4      
#                    leg_5, leg_6 
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------  
def plot_6(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6,
               leg_1, leg_2, leg_3, leg_4, leg_5, leg_6,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue' , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'green', linestyle = '-'  )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'brown', linestyle = '-'  ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'  , linestyle = '-'  )
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'black', linestyle = '-.' )      
    ax.plot(prr_6.index, prr_6, label = leg_6, color = 'black', linestyle = '--' )    
      
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_5)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True,  which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)

# end def plot_6
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# plot_7
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 6 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                    prr_5, prr_6       index and appropriate values)
#                    prr_7              index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4      
#                    leg_5, leg_6 
#                    leg_7
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------  
def plot_7(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, prr_7,
               leg_1, leg_2, leg_3, leg_4, leg_5, leg_6, leg_7,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue' , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'green', linestyle = '-'  )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'brown', linestyle = '-'  ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'  , linestyle = '-'  )
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'black', linestyle = '-.' )      
    ax.plot(prr_6.index, prr_6, label = leg_6, color = 'black', linestyle = '--' )     
    
    ax.plot(prr_7.index, prr_7, label = leg_7, color = 'yellow') 
      
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind,
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    # Gap betweet axis 
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(12)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_5)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)
# end def plot_7
#------------------------------------------------------------------------------


# For daily task


#------------------------------------------------------------------------------
# plot_2d
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 2 lines in a single plot 
#
# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                                       dapa plot (timeseries have to have a time
#                                       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    na_3, na4        - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------
def plot_2d(ax, prr_1, prr_2,
                leg_1, leg_2, 
                na_3, na_4, na_5, date_ind, nst, l_p, 
                pr_3, pr_4, pr_5, time_step_1, time_step_2):    
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'tab:blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'tab:orange', linestyle = '--')
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind,
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
  
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(xftm)
    #ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_6)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)
# end def plot_2d
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# plot_3
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 3 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3              dapa plot (timeseries have to have a time
#                                       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3       
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------ 


def plot_3d(ax, prr_1, prr_2, prr_3,
                leg_1, leg_2, leg_3,
                na_3, na_4, na_5, date_ind, nst, l_p,
                pr_3, pr_4, pr_5, time_step_1, time_step_2):   
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'tab:blue'  , linestyle = '-' )   
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'tab:orange', linestyle = '--')    
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'tab:green' , linestyle = '-.')
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which = 'major', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which = 'minor', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
  
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(xftm)
    #ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_7)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)
# end def plot_3d
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# plot_4
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 4 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                                       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4       
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------
def plot_4d(ax, prr_1, prr_2, prr_3, prr_4,
                leg_1, leg_2, leg_3, leg_4,
                na_3, na_4, na_5, date_ind, nst, l_p,
                pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', 
                                                                     alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , 
                                                                     alpha = 0.6 )    
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind,
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which = 'major', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which = 'minor', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
  
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(xftm)
    #ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_8)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)    
# end def plot_4d
#------------------------------------------------------------------------------
    
#------------------------------------------------------------------------------
# plot_5
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 5 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                    prr_5              index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4      
#                    leg_5 
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------    
def plot_5d(ax, prr_1, prr_2, prr_3, prr_4, prr_5, 
                leg_1, leg_2, leg_3, leg_4, leg_5,
                na_3, na_4, na_5, date_ind, nst,
                l_p, pr_3, pr_4, pr_5, time_step_1, time_step_2):    
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'     , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange'   , linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green'    , linestyle = '-.',
                                                                        alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'      , linestyle = ':' ,
                                                                        alpha = 0.6 )     
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'tab:brown', linestyle = '-.')
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which = 'major', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which = 'minor', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
  
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(xftm)
    #ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_9)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)  
# end def plot_5d
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# plot_6
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 6 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                    prr_5, prr_6       index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4      
#                    leg_5, leg_6 
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------ 
def plot_6d(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, 
                leg_1, leg_2, leg_3, leg_4, leg_5, leg_6,                
                na_3, na_4, na_5, date_ind, nst,
                l_p, pr_3, pr_4, pr_5, time_step_1, time_step_2):    
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', 
                                                                     alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' ,
                                                                     alpha = 0.6 )       
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'tab:brown' , linestyle = '-.')    
    ax.plot(prr_6.index, prr_6, label = leg_6, color = 'lime'      , linestyle = '-' )    
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind,
                 color = 'black', fontsize = 14, pad = 20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which = 'major', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which = 'minor', bottom = True  , top = False,
                   left = True, right = True   , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
  
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%H')
    ax.xaxis.set_major_formatter(xftm)
    #ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(0)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
    yax.set_minor_locator(minorLocator_10)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True , which = 'major', color = 'k'   , linestyle = 'solid' , alpha = 0.5)  
# end def plot_6d
#------------------------------------------------------------------------------


# Statistical sections

#------------------------------------------------------------------------------
# Subroutine: get_m
#------------------------------------------------------------------------------
# The subroutine needs for getting actual plot for parameters (Average montly values)
# 
# Input parameters : df       - dataset with COSMO data (COSMO_CTR)
#                    df2      - dataset with COSMO data (COSMO_v3.5)  
#                    df3      - dataset with COSMO data (COSMO_v4.5)
#                    df4      - dataset with COSMO data (COSMO_v4.5e)
#                    df5      - dataset with in-situ, reanalysis, satellite data
#                    param    - parameter from COSMO
#                    name_2   - label for Y-axis
#                    data_out - path for output
#                    y1       - min values for y-axis
#                    y2       - max values for Y-axis
#                    step     - step between y1 and y2
#                    status   - the domain territory    
#
# Output parameters: Plot with parameters
#------------------------------------------------------------------------------

def get_m(df, df2, df3, df4, df5, param, name_2, data_out, y1, y2, step, status):
    #print (status)
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    plt.plot(df.index ,  df[param], label = 'CCLMref'  , color = 'blue'  , linestyle = '-' )
    plt.plot(df2.index, df2[param], label = 'CCLMv3.5' , color = 'green' , linestyle = '-' ) #, linewidth = 2)
    plt.plot(df3.index, df3[param], label = 'CCLMv4.5' , color = 'brown' , linestyle = '-' ) #, alpha = 0.4 , linewidth = 2)
    plt.plot(df4.index, df4[param], label = 'CCLMv4.5e', color = 'red'   , linestyle = '-' ) #, alpha = 0.6 , linewidth = 2)    
    
    if param == 'ALHFL_S':
        plt.plot(df5.index, df5['LE'], label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'ASHFL_S': 
        plt.plot(df5.index, df5['H'] , label = 'OBS', color = 'black', linestyle = ':')            
    elif param == 'AEVAP_S':
        plt.plot(df5.index, df5['Et_a'], label = 'Gleam_v3.5a', color = 'black', linestyle = ':'  )                # was Ep_a
        plt.plot(df5.index, df5['Et_b'], label = 'Gleam_v3.5b', color = 'black', linestyle = '--' )                # was Ep_b   
    elif param == 'ZVERBO':
        plt.plot(df5.index, df5['Ep_a'], label = 'Gleam_v3.5a', color = 'black', linestyle = ':'  )                # was Et_a
        plt.plot(df5.index, df5['Ep_b'], label = 'Gleam_v3.5b', color = 'black', linestyle = '--' )                # was Et_b      
    elif param == 'T_2M': 
        plt.plot(df5.index, df5['T_2M'], label = 'obs', color = 'black', linestyle = ':')
    elif param == 'T_S': 
        plt.plot(df5.index, df5['TS']  , label = 'obs', color = 'black', linestyle = ':')
    elif param == 'TMAX_2M': 
        plt.plot(df5.index, df5['TMAX'], label = 'obs', color = 'black', linestyle = ':')
    elif param == 'TMIN_2M': 
        plt.plot(df5.index, df5['TMIN'], label = 'obs', color = 'black', linestyle = ':')    
        
    font = font_manager.FontProperties(family = 'Arial', style  = 'normal', size = 16)    
        
    ax.legend(prop = font, loc = 'upper right')
    
    if status == '1':
        ax.set_title('Domain: Parc' + '     ' + 'Station: Rollesbroich',
                     color = 'black', fontsize = 18, pad = 20) 

    elif status == '2':    
        ax.set_title('Domain: Linden'    + '     ' + 'Station: Linden',
                     color = 'black', fontsize = 18, pad = 20)    
    elif status == '3':
        ax.set_title('Domain: Lindenberg' + '     ' + 'Station: Lindenberg',
                     color = 'black', fontsize = 18, pad = 20)    

        
    ax.set_ylabel(name_2, color = 'black', fontsize = 16, labelpad = 20)

    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(18)
    
    plt.grid()
    
    plt.savefig(data_out + 'Annual/' +param + '_annual.png', format = 'png', dpi = 300)

    plt.close(fig)        
    plt.gcf().clear() 
#------------------------------------------------------------------------------    

  
#------------------------------------------------------------------------------
# Subroutine: get_d
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
#
# Input parameters : df           - dataset with COSMO data (COSMO_CTR)
#                    df2          - dataset with COSMO data (COSMO_v3.5)  
#                    df3          - dataset with COSMO data (COSMO_v4.5)
#                    df4          - dataset with COSMO data (COSMO_v4.5e)
#                    df5          - dataset with in-situ, reanalysis, satellite data
#                    param        - parameter from COSMO
#                    name_2       - label for Y-axis
#                    data_out     - path for output
#                    y1           - min values for y-axis
#                    y2           - max values for Y-axis
#                    step         - step between y1 and y2
#                    intup_region - the domain territory    
#
#
# Output parameters: Plot with parameters
#------------------------------------------------------------------------------
   
def get_d(df, df2, df3, df4, df_obs, param, name_2, data_out, y1, y2, step, input_region):
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)
  
    plt.plot(df.index ,  df[param], label = 'CCLMref'  , color = 'blue'  , linestyle = '-' )
    plt.plot(df2.index, df2[param], label = 'CCLMv3.5' , color = 'green' , linestyle = '-' ) #, linewidth = 2)
    plt.plot(df3.index, df3[param], label = 'CCLMv4.5' , color = 'brown' , linestyle = '-' ) #, alpha = 0.4 , linewidth = 2)
    plt.plot(df4.index, df4[param], label = 'CCLMv4.5e', color = 'red'   , linestyle = '-' ) #, alpha = 0.6 , linewidth = 2)    
    
    if param == 'ALHFL_S':
        plt.plot(df_obs.index, df_obs['LE'], label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'ASHFL_S': 
        plt.plot(df_obs.index, df_obs['H'] , label = 'OBS', color = 'black', linestyle = ':')            
    elif param == 'AEVAP_S':
        plt.plot(df_obs.index, df_obs['Et_a'], label = 'Gleam_v3.5a', color = 'black', linestyle = ':'  )                # was Ep_a
        plt.plot(df_obs.index, df_obs['Et_b'], label = 'Gleam_v3.5b', color = 'black', linestyle = '--' )                # was Ep_b   
    elif param == 'ZVERBO':
        plt.plot(df_obs.index, df_obs['Ep_a'], label = 'Gleam_v3.5a', color = 'black', linestyle = ':'  )                # was Et_a
        plt.plot(df_obs.index, df_obs['Ep_b'], label = 'Gleam_v3.5b', color = 'black', linestyle = '--' )                # was Et_b      
    elif param == 'T_2M': 
        plt.plot(df_obs.index, df_obs['T_2M'], label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'T_S': 
        plt.plot(df_obs.index, df_obs['TS']  , label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'TMAX_2M': 
        plt.plot(df_obs.index, df_obs['TMAX'], label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'TMIN_2M': 
        plt.plot(df_obs.index, df_obs['TMIN'], label = 'OBS', color = 'black', linestyle = ':')   

        
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
        label.set_fontsize(18)
    
    plt.grid()
    
    plt.savefig(data_out + 'Monthly/' + param + '_June.png', format = 'png', dpi = 300)
    
    plt.close(fig)        
    plt.gcf().clear() 
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# Subroutine: get_d
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
#
# Input parameters : df           - dataset with COSMO data (COSMO_CTR)
#                    df2          - dataset with COSMO data (COSMO_v3.5)  
#                    df3          - dataset with COSMO data (COSMO_v4.5)
#                    df4          - dataset with COSMO data (COSMO_v4.5e)
#                    df5          - dataset with in-situ, reanalysis, satellite data
#                    param        - parameter from COSMO
#                    name_2       - label for Y-axis
#                    data_out     - path for output
#                    y1           - min values for y-axis
#                    y2           - max values for Y-axis
#                    step         - step between y1 and y2
#                    intup_region - the domain territory    
#
#
# Output parameters: Plot with parameters
#------------------------------------------------------------------------------

def get_data_m(ax, df_ref, df_v35, df_v45, df_v45e, df_v35a, df_v35b, df_obs,
               param, name_2, input_region, y1, y2, step, time_step,
               text_values, settings = True, legendary = True):

    if time_step == 'D':
        # One day step
        x_values  = np.arange( 0 , len(df_ref) + 1, 31)                            # Define the intervals for x axis (main ticks)  
        x_values2 = np.arange( 14, len(df_ref) + 1, 31)                            # Define the intervals for x axis (minor ticks) 
    elif time_step == '2D':
        # Two day step
        x_values  = np.arange( 0   , len(df_ref) + 1, 15)                            # Define the intervals for x axis (main ticks)  
        x_values2 = np.arange( 7.5 , len(df_ref) + 1, 15)                            # Define the intervals for x axis (minor ticks) 
    else:
        # Five day step
        x_values  = np.arange( 0 , len(df_ref) + 1, 6)                            # Define the intervals for x axis (main ticks)  
        x_values2 = np.arange( 3 , len(df_ref) + 1, 6)                            # Define the intervals for x axis (minor ticks)
   
    ax.plot(df_ref.index , df_ref , label = 'CCLMref'  , color = 'blue'  , linestyle = '-' )
    ax.plot(df_v35.index , df_v35 , label = 'CCLMv3.5' , color = 'green' , linestyle = '-' )
    ax.plot(df_v45.index , df_v45 , label = 'CCLMv4.5' , color = 'brown' , linestyle = '-' )
    ax.plot(df_v45e.index, df_v45e, label = 'CCLMv4.5e', color = 'red'   , linestyle = '-' )


    if param in ('AEVAP_S', 'ZVERBO'):
        ax.plot(df_v35a.index, df_v35a, label = 'GLEAM v3.5a', color = 'black', linestyle = ':'  )                # was Ep_a
        ax.plot(df_v35b.index, df_v35b, label = 'GLEAM v3.5b', color = 'black', linestyle = '--' )                # was Ep_b   
    elif param in ('T_2M', 'T_S', 'TMAX_2M', 'TMIN_2M'):
        ax.plot(df_obs.index, df_obs, label = 'OBS', color = 'black', linestyle = ':')
    
    

    # Settings for plot         


    # Set y-axis    
    ax.set_ylabel(name_2, color = 'black', fontsize = 14, labelpad = 50)
    
    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))
    #ax.tick_params(axis='y', which='major', pad = 30)

    ax.tick_params(axis='y', which ='major',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on', pad = 30)
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False, left = True, right = True, labelleft ='on', labelright = 'on', pad = 30)
    # Set x-axis
    ax.get_xticks()      
    ax.set_xticks(x_values)        
    ax.xaxis.set_major_formatter(ticker.NullFormatter())

    
    if legendary == True:
        font = font_manager.FontProperties(family = 'Arial', style  = 'normal', size = 14)    
        ax.legend(prop = font, loc='upper center', bbox_to_anchor=(0.5, 2.5),
                  ncol=6, fancybox=True, shadow=False)
            
    if settings == True:
              
        ax.xaxis.set_minor_locator(ticker.FixedLocator([x_values2[0],
                                                        x_values2[1],
                                                        x_values2[2],
                                                        x_values2[3],
                                                        x_values2[4],
                                                        x_values2[5],]))
        
        
        ax.xaxis.set_minor_formatter(ticker.FixedFormatter([text_values[0],
                                                            text_values[1],
                                                            text_values[2],
                                                            text_values[3],
                                                            text_values[4],
                                                            text_values[5]]))
    
        ax.tick_params(axis='both', which='minor', labelsize=16)     
    
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
        label.set_horizontalalignment('center')
        
    ax.grid()

"""
def get_data_m(df_ref, df_v35, df_v45, df_v45e, df_obs,
               param, name_2, input_region, y1, y2, step, 
               text_values, data_out):

    
    # One day step
    #x_values  = np.arange( 0 , len(df_ref) + 1, 31)                            # Define the intervals for x axis (main ticks)  
    #x_values2 = np.arange( 14, len(df_ref) + 1, 31)                            # Define the intervals for x axis (minor ticks) 
    
    # Two day step
    x_values  = np.arange( 0 , len(df_ref) + 1, 6)                            # Define the intervals for x axis (main ticks)  
    x_values2 = np.arange( 3 , len(df_ref) + 1, 6)                            # Define the intervals for x axis (minor ticks) 
    
    fig = plt.figure(figsize = (14,10))  
    ax  = fig.add_subplot(111)
    
    plt.plot(df_ref.index , df_ref[param] , label = 'CCLMref'  , color = 'blue'  , linestyle = '-' )
    plt.plot(df_v35.index , df_v35[param] , label = 'CCLMv3.5' , color = 'green' , linestyle = '-' )
    plt.plot(df_v45.index , df_v45[param] , label = 'CCLMv4.5' , color = 'brown' , linestyle = '-' )
    plt.plot(df_v45e.index, df_v45e[param], label = 'CCLMv4.5e', color = 'red'   , linestyle = '-' )

   
    if param == 'T_2M': 
        plt.plot(df_obs.index, df_obs['T_2M'], label = 'obs', color = 'black', linestyle = ':')
    elif param == 'T_S': 
        plt.plot(df_obs.index, df_obs['TS']  , label = 'obs', color = 'black', linestyle = ':')
    elif param == 'TMAX_2M': 
        plt.plot(df_obs.index, df_obs['TMAX'], label = 'obs', color = 'black', linestyle = ':')
    elif param == 'TMIN_2M': 
        plt.plot(df_obs.index, df_obs['TMIN'], label = 'obs', color = 'black', linestyle = ':')   
    elif param == 'AEVAP_S':
        plt.plot(df_obs.index, df_obs['Ep_a'], label = 'Gleam_v3.5a', color = 'black', linestyle = ':'  )                # was Ep_a
        plt.plot(df_obs.index, df_obs['Ep_b'], label = 'Gleam_v3.5b', color = 'black', linestyle = '--' )                # was Ep_b   
    elif param == 'ZVERBO':
        plt.plot(df_obs.index, df_obs['Et_a'], label = 'Gleam_v3.5a', color = 'black', linestyle = ':'  )                # was Et_a
        plt.plot(df_obs.index, df_obs['Et_b'], label = 'Gleam_v3.5b', color = 'black', linestyle = '--' )                # was Et_b  
        
    
    # Settings for plot         
    ax.legend()

    if input_region == '1':
        ax.set_title('Daily values of ' + param + ' in June from 2010 to 2015' +
                     '\n\n' + 'Domain: Parc' + '     ' + 'Station: Rollesbroich',
                     color = 'black', fontsize = 14, pad = 20) 

    elif input_region == '2':    
        ax.set_title('Daily values of ' + param + ' in June from 2010 to 2015' +
                     '\n\n' + 'Domain: Linden'  + '     ' + 'Station: Linden',
                     color = 'black', fontsize = 14, pad = 20)    
    else:
        ax.set_title('Daily values of ' + param + ' in June from 2010 to 2015' +
                     '\n\n' + 'Domain: Lindenberg' + '     ' + 'Station: Lindenberg',
                     color = 'black', fontsize = 14, pad = 20)    
    
    # Set y-axis    
    ax.set_ylabel(name_2, color = 'black', fontsize = 14, labelpad = 20)    
    ax.get_yticks()
    ax.set_yticks(np.arange(y1, y2, step))


    # Set x-axis
    ax.get_xticks()      
    #ax.set_xticks(np.arange(0, 180.1, 30))   
    ax.set_xticks(x_values)
        
    ax.xaxis.set_major_formatter(ticker.NullFormatter())
    #ax.xaxis.set_minor_locator(ticker.FixedLocator([14, 44, 74, 104, 134, 164]))
    ax.xaxis.set_minor_locator(ticker.FixedLocator([x_values2[0],
                                                    x_values2[1],
                                                    x_values2[2],
                                                    x_values2[3],
                                                    x_values2[4],
                                                    x_values2[5],]))
    
    
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter([text_values[0],
                                                        text_values[1],
                                                        text_values[2],
                                                        text_values[3],
                                                        text_values[4],
                                                        text_values[5]]))
    
    ax.tick_params(axis='both', which='minor', labelsize=16)     
    
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(30)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(18)

    plt.grid()    
    plt.savefig(data_out + 'test/' + param + '_June.png', format = 'png', dpi = 300)
    
    plt.close(fig)        
    plt.gcf().clear() 
"""
#------------------------------------------------------------------------------





















#------------------------------------------------------------------------------
# Subroutine: get_plot_h
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
#
# Input parameters : df           - dataset with COSMO data (COSMO_CTR)
#                    df2          - dataset with COSMO data (COSMO_v3.5)  
#                    df3          - dataset with COSMO data (COSMO_v4.5)
#                    df4          - dataset with COSMO data (COSMO_v4.5e)
#                    df5          - dataset with in-situ, reanalysis, satellite data
#                    df6          - dataset with GLEAM data (point)    
#                    param        - parameter from COSMO
#                    name_2       - label for Y-axis
#                    data_out     - path for output
#                    y1           - min values for y-axis
#                    y2           - max values for Y-axis
#                    step         - step between y1 and y2
#                    intup_region - the domain territory    
#
# Output parameters: Plot with parameters
#------------------------------------------------------------------------------

def get_h(df_ref, df_v35, df_v45, df_v45e, df_obs, 
          param, name_2, data_out, y1, y2, step, input_region):
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    plt.plot(df_ref.index , df_ref[param] , label = 'CCLMref'  , color = 'blue'  , linestyle = '-' )
    plt.plot(df_v35.index , df_v35[param] , label = 'CCLMv3.5' , color = 'green' , linestyle = '-' )
    plt.plot(df_v45.index , df_v45[param] , label = 'CCLMv4.5' , color = 'brown' , linestyle = '-' )
    plt.plot(df_v45e.index, df_v45e[param], label = 'CCLMv4.5e', color = 'red'   , linestyle = '-' ) 

    if param == 'ALHFL_S':
        plt.plot(df_obs.index, df_obs['LE'], label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'ASHFL_S': 
        plt.plot(df_obs.index, df_obs['H'] , label = 'OBS', color = 'black', linestyle = ':')       

   
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
        label.set_fontsize(18)
    
    plt.grid()
    
    plt.savefig(data_out +'Diurnal/' + param + '_Hour.png', format = 'png', dpi = 300)
    plt.close(fig)        
    plt.gcf().clear() 
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Subroutine: get_u
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual plot for parameters (Average daily values)
# 
# Input parameters : df           - dataset with COSMO data (COSMO_CTR)
#                    df2          - dataset with COSMO data (COSMO_v3.5)  
#                    df3          - dataset with COSMO data (COSMO_v4.5)
#                    df4          - dataset with COSMO data (COSMO_v4.5e)
#                    df5          - dataset with in-situ, reanalysis, satellite data
#                    param        - parameter from COSMO
#                    name_2       - label for Y-axis
#                    data_out     - path for output
#                    y1           - min values for y-axis
#                    y2           - max values for Y-axis
#                    step         - step between y1 and y2
#                    intup_region - the domain territory     
#
# Output parameters: Plot with parameters
#------------------------------------------------------------------------------

def get_u(df_ref, df_v35, df_v45, df_v45e, df_obs, param,
          name_2, data_out, y1, y2, step, input_region):
    
    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    plt.plot(df_ref.index , df_ref[param] , label = 'CCLMref'  , color = 'blue'  , linestyle = '-' )
    plt.plot(df_v35.index , df_v35[param] , label = 'CCLMv3.5' , color = 'green' , linestyle = '-' )
    plt.plot(df_v45.index , df_v45[param] , label = 'CCLMv4.5' , color = 'brown' , linestyle = '-' )
    plt.plot(df_v45e.index, df_v45e[param], label = 'CCLMv4.5e', color = 'red'   , linestyle = '-' ) 
        
   
    if param == 'ALHFL_S':
        plt.plot(df_obs.index, df_obs['LE'], label = 'OBS', color = 'black', linestyle = ':')
    elif param == 'ASHFL_S': 
        plt.plot(df_obs.index, df_obs['H'] , label = 'OBS', color = 'black', linestyle = ':')          
    else:
        print('no additional parameters')        
    #elif param == 'AEVAP_S':
    #    plt.scatter(df6.index, df6['Ep_a']     , label = 'Gleam_v3.5a'   , color = 'magenta', alpha = 0.5)
    #    plt.scatter(df6.index, df6['Ep_b']     , label = 'Gleam_v3.5b'   , color = 'lime'   , alpha = 0.5)    
    #elif param == 'ZVERBO':
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
# Input parameters : ts_main   - the main timeseries with data
#                    ts_hot    - timeseries with extrem hot  periods   
#                    ts_cold   - timeseries with extrem cold periods
#                    interval  - time period
#                    domain    - research territory
#                    station   - Meteorological station
#                    x_start   - the date of the start period
#                    x_stop    - the date of the end period
#                    data_exit - path for results
#
#------------------------------------------------------------------------------
def plot_waves(ts_main, ts_hot, ts_cold, interval, domain, station, x_start, 
               x_stop, data_exit, cosmo_type):

    fig = plt.figure(figsize = (14,10))
    ax  = fig.add_subplot(111)

    if cosmo_type == True:
        plt.plot(ts_main.index, ts_main, label = 'T2_M COSMO' , color = 'blue' , 
                                                                linestyle = '-')
    else:
        plt.plot(ts_main.index, ts_main, label = 'T2_M HYRAS' , color = 'green', 
                                                               linestyle = '-')
    
    
    plt.scatter(ts_hot.index ,  ts_hot , label = 'hot wave' , color = 'red'   ,
                                                               linewidths = 2 )
    plt.scatter(ts_cold.index,  ts_cold, label = 'cold wave', color = 'orange',
                                                               linewidths = 2 )

    ax.legend(loc = 'lower right', frameon=True)
    
    ax.set_title('Heat and cold waves ' + interval + 
                 '\n\n' + 'Domain: '    + domain   + '     ' + 'Station: ' + station,
                 color = 'black', fontsize = 14, pad = 20)    

    ax.set_ylabel('Standart deviation', color = 'black', fontsize = 14, labelpad = 20)
    ax.set_xlabel('Years'             , color = 'black', fontsize = 14, labelpad = 20)

    ax.get_xticks()
    ax.set_xticks(pd.date_range(x_start, x_stop, freq = '2M')) #'2MS')) #freq = 'YS'))

    ax.get_yticks()
    ax.set_yticks(np.arange(-2.5, 2.51, 0.5))

    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(90)
        label.set_fontsize(14)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(14)
            
    plt.grid()

    if cosmo_type == True:   
        plt.savefig(data_exit + 'Waves_' + interval +' COSMO.png', format = 'png', dpi = 300) 
    else:
        plt.savefig(data_exit + 'Waves_' + interval +' HYRAS.png', format = 'png', dpi = 300)        
#------------------------------------------------------------------------------    
    
    

#------------------------------------------------------------------------------
# Subroutine: Taylor diagram 
#------------------------------------------------------------------------------
#
# The subroutine needs for getting plot with information about heat and cold waves
#
# Acknowledgment: Yannick Copin
#------------------------------------------------------------------------------

class TaylorDiagram(object):
    """
    Taylor diagram.
    Plot model standard deviation and correlation to reference (data)
    sample in a single-quadrant polar plot, with r=stddev and
    theta=arccos(correlation).
    """

    def __init__(self, refstd,
                 fig=None, rect=111, label='_', srange=(0, 1.5), extend=False):
        """
        Set up Taylor diagram axes, i.e. single quadrant polar
        plot, using `mpl_toolkits.axisartist.floating_axes`.
        Parameters:
        * refstd: reference standard deviation to be compared to
        * fig: input Figure or None
        * rect: subplot definition
        * label: reference label
        * srange: stddev axis extension, in units of *refstd*
        * extend: extend diagram to negative correlations
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF

        self.refstd = refstd            # Reference standard deviation

        tr = PolarAxes.PolarTransform()

        # Correlation labels
        rlocs = np.array([0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1])
        if extend:
            # Diagram extended to negative correlations
            self.tmax = np.pi
            rlocs = np.concatenate((-rlocs[:0:-1], rlocs))
        else:
            # Diagram limited to positive correlations
            self.tmax = np.pi/2
        tlocs = np.arccos(rlocs)        # Conversion to polar angles
        gl1 = GF.FixedLocator(tlocs)    # Positions
        tf1 = GF.DictFormatter(dict(zip(tlocs, map(str, rlocs))))

        # Standard deviation axis extent (in units of reference stddev)
        self.smin = srange[0] * self.refstd
        self.smax = srange[1] * self.refstd

        ghelper = FA.GridHelperCurveLinear(
            tr,
            extremes = (0, self.tmax, self.smin, self.smax),
                        grid_locator1=gl1, tick_formatter1=tf1)

        if fig is None:
            fig = plt.figure()

        ax = FA.FloatingSubplot(fig, rect, grid_helper = ghelper)
        fig.add_subplot(ax)

        # Adjust axes
        ax.axis["top"].set_axis_direction("bottom")   # "Angle axis"
        ax.axis["top"].toggle(ticklabels = True, label = True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].major_ticklabels.set_color("b")
        ax.axis["top"].major_ticklabels.set_size(14)
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")
        ax.axis["top"].label.set_color("b")
        ax.axis["top"].label.set_fontsize(14)

        ax.axis["left"].set_axis_direction("bottom")  # "X axis"
        ax.axis["left"].label.set_text("Normalized Standard Deviation")
        ax.axis["left"].label.set_fontsize(14)
        ax.axis["left"].major_ticklabels.set_color("k")
        ax.axis["left"].major_ticklabels.set_size(14)


        ax.axis["right"].set_axis_direction("top")    # "Y-axis"
        ax.axis["right"].toggle(ticklabels=True)
        ax.axis["right"].major_ticklabels.set_axis_direction(
            "bottom" if extend else "left")
        ax.axis["right"].major_ticklabels.set_color("k")
        ax.axis["right"].major_ticklabels.set_size(14)


        if self.smin:
            ax.axis["bottom"].toggle(ticklabels=False, label=False)
        else:
            ax.axis["bottom"].set_visible(False)          # Unused

        self._ax = ax                   # Graphical axes
        self.ax = ax.get_aux_axes(tr)   # Polar coordinates

        # Add reference point and stddev contour
        l, = self.ax.plot([0], self.refstd, 'b*',
                          ls = '', ms = 16, label = label)
        t = np.linspace(0, self.tmax)
        r = np.zeros_like(t) + self.refstd
        self.ax.plot(t, r, 'k--', label='_')

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = [l]

    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """
        Add sample (*stddev*, *corrcoeff*) to the Taylor
        diagram. *args* and *kwargs* are directly propagated to the
        `Figure.plot` command.
        """

        l, = self.ax.plot(np.arccos(corrcoef), stddev,
                          *args, **kwargs)  # (theta, radius)
        self.samplePoints.append(l)

        return l

    def add_grid(self, *args, **kwargs):
        """Add a grid."""

        self._ax.grid(*args, **kwargs)

    def add_contours(self, levels = 5, **kwargs):
        """
        Add constant centered RMS difference contours, defined by *levels*.
        """

        rs, ts = np.meshgrid(np.linspace(self.smin, self.smax),
                             np.linspace(0, self.tmax))
        # Compute centered RMS difference
        rms = np.sqrt(self.refstd**2 + rs**2 - 2*self.refstd*rs*np.cos(ts))

        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)

        return contours


   
    
   
    
   
    
#------------------------------------------------------------------------------
# plot_5
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 5 lines in a single plot 

# Input parameters:  ax               - work area
#                    prr_1, prr_2     - the main parameters which are using for
#                    prr_3, prr_4       dapa plot (timeseries have to have a time
#                    prr_5              index and appropriate values)
#                                       index has to be in format - datetime
#                    leg_1, leg_2     - the name of parameters for legend
#                    leg_3, leg_4      
#                    leg_5 
#                    na_3, na_4       - name of plot (label) and Y-axis
#                    date_ind         - timeperiod (label)
#                    nst              - the name of meteorological station(label)
#                    l_p              - legend position
#                    pr_3, pr_4, pr_5 - data scales of data range  
#                    time_step_1      - time start   
#                    time_step_2      - time stop 
#------------------------------------------------------------------------------   
def plot_5_stom(ax, prr_1, prr_2, prr_3, prr_4, prr_5, 
                leg_1, leg_2, leg_3, leg_4, leg_5,
                na_3, na_4, date_ind, nst, l_p,
                pr_3, pr_4, pr_5, time_step_1, time_step_2, station_plot): 
    """
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'black'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'blue'   , linestyle = '--' , linewidth = 2)
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green'  , linestyle = '-.' , 
                                                                      alpha = 0.4 , linewidth = 2) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'    , linestyle = ':'  , 
                                                                      alpha = 0.6 , linewidth = 2)
    ax.scatter(prr_5.index, prr_5, label = leg_5, color = 'cyan',  linewidths = 3.5 )
    
    # Plot colours for Merja
    """
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue' , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'green', linestyle = '-'  ) #, linewidth = 2)
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'brown', linestyle = '-' ) #, alpha = 0.4 , linewidth = 2) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'  , linestyle = '-' ) # , alpha = 0.6 , linewidth = 2)    
    ax.scatter(prr_5.index, prr_5, label = leg_5, color = 'black',  linewidths = 3.5 )
    

    
    ax.set_title('Domain: ' + nst + '    Station: ' + station_plot, 
                 color = 'black', fontsize = 18, pad = 20)
    
    ax.set_ylabel(na_4, color = 'black', fontsize = 16, labelpad = 20)
    
    font = font_manager.FontProperties(family = 'Arial', style  = 'normal', size = 16)    
        
    ax.legend(prop = font, loc = l_p)
    
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis = 'y' , which ='major', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    ax.tick_params(axis = 'y' , which ='minor', bottom = True  , top = False,
                   left = True, right = True  , labelleft ='on', labelright = 'on')
    # Gap betweet axis
    for tick in ax.get_xaxis().get_major_ticks():
        tick.set_pad(12.)
        tick.label1 = tick._get_text1()
        
    xax = ax.xaxis
    yax = ax.yaxis
    #ax.set_xticks(pd.date_range(time_step_1, time_step_2, freq = '1M'))
    #ax.set_xlim(time_step_1, time_step_2)
    xftm = mdates.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xftm)
    ax.xaxis.set_minor_locator(days)
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(15)
        label.set_fontsize(16)
    for label in ax.yaxis.get_ticklabels():
        label.set_color('black')
        label.set_fontsize(18)
    yax.set_minor_locator(minorLocator_4)
    yax.set_minor_formatter(NullFormatter())
    xax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2)
    yax.grid(True, which = 'minor', color = 'grey', linestyle = 'dashed', alpha = 0.2) 
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    
# end def plot_5
#------------------------------------------------------------------------------   

   
    
    
    
    
    
    
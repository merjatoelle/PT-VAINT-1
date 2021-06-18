# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:32:32 2021

@author: churiulin
"""




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams 
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator, NullFormatter

import gc

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




#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 2 lines in a single plot 

# prr_1, prr_2 - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------
def plot_2(ax, prr_1, prr_2,
               leg_1, leg_2, 
               na_3, na_4, date_ind, nst, l_p, 
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 

    ax.plot(prr_1.index, prr_1, label = leg_1 , color = 'tab:blue'  , linestyle = '-' )   
    ax.plot(prr_2.index, prr_2, label = leg_2 , color = 'tab:orange', linestyle = '--')   
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
# Subroutine for data visualization: Option for 3 lines in a single plot 

# prr_1, prr_2, prr_3  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------
        
def plot_3(ax, prr_1, prr_2, prr_3, 
               leg_1, leg_2, leg_3,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1 , color = 'tab:blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2 , color = 'tab:orange', linestyle = '--')
    ax.plot(prr_3.index, prr_3, label = leg_3 , color = 'tab:green' , linestyle = '-.')
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

# end def plot_3
#------------------------------------------------------------------------------
    

#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 4 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------



def plot_4(ax, prr_1, prr_2, prr_3, prr_4,
               leg_1, leg_2, leg_3, leg_4,
               na_3, na_4, date_ind, nst, l_p, 
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
# Subroutine for data visualization: Option for 5 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4, prr_5  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4, leg_5 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------

    
def plot_5(ax, prr_1, prr_2, prr_3, prr_4, prr_5, 
               leg_1, leg_2, leg_3, leg_4, leg_5,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'black' , linestyle = '-.', alpha = 0.5 )
   
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, 
                 color = 'black', fontsize = 14, pad = 20)
    
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)
    
# end def plot_5
#------------------------------------------------------------------------------ 
    
 
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 6 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4, prr_5, prr_6  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4, leg_5, leg_6 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------  
  
def plot_6(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6,
               leg_1, leg_2, leg_3, leg_4, leg_5, leg_6,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )  
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'sienna'    , linestyle = '--', alpha = 0.6 )      
    ax.plot(prr_6.index, prr_6, label = leg_6, color = 'tab:purple', linestyle = '-.', linewidth = 0.9)    
      
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

# end def plot_6
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 6 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4, prr_5, prr_6  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4, leg_5, leg_6 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------  
  
def plot_7(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, prr_7,
               leg_1, leg_2, leg_3, leg_4, leg_5, leg_6, leg_7,
               na_3, na_4, date_ind, nst, l_p,
               pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )  
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'sienna'    , linestyle = '--', alpha = 0.6 )      
    ax.plot(prr_6.index, prr_6, label = leg_6, color = 'tab:purple', linestyle = '-.', linewidth = 0.9)    
    ax.plot(prr_7.index, prr_7, label = leg_7, color = 'black'     , alpha = 0.7) 
      
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind,
                 color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad = 20)
    ax.legend(loc = l_p, frameon=False)  
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

# end def plot_6
#------------------------------------------------------------------------------

# For daily task

#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 2 lines in a single plot 

# prr_1, prr_2 - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------


def plot_2d(ax, prr_1, prr_2,
                leg_1, leg_2, 
                na_3, na_4, na_5, date_ind, nst, l_p, 
                pr_3, pr_4, pr_5, time_step_1, time_step_2):    
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'tab:blue'  , linestyle = '-' )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'tab:orange', linestyle = '--')
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

# end def plot_2d
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 3 lines in a single plot 

# prr_1, prr_2, prr_3  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------


def plot_3d(ax, prr_1, prr_2, prr_3,
                leg_1, leg_2, leg_3,
                na_3, na_4, na_5, date_ind, nst, l_p,
                pr_3, pr_4, pr_5, time_step_1, time_step_2):   
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'tab:blue'  , linestyle = '-' )   
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'tab:orange', linestyle = '--')    
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'tab:green' , linestyle = '-.')
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)

# end def plot_3d
#------------------------------------------------------------------------------


    
#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 4 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------
   
def plot_4d(ax, prr_1, prr_2, prr_3, prr_4,
                leg_1, leg_2, leg_3, leg_4,
                na_3, na_4, na_5, date_ind, nst, l_p,
                pr_3, pr_4, pr_5, time_step_1, time_step_2): 
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )    
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)    

# end def plot_4d
#------------------------------------------------------------------------------
    

#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 5 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4, prr_5  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4, leg_5 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------  


def plot_5d(ax, prr_1, prr_2, prr_3, prr_4, prr_5, 
                leg_1, leg_2, leg_3, leg_4, leg_5,
                na_3, na_4, na_5, date_ind, nst,
                l_p, pr_3, pr_4, pr_5, time_step_1, time_step_2):    
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )     
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'tab:brown' , linestyle = '-.')
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)  
    
# end def plot_5d
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine for data visualization: Option for 6 lines in a single plot 

# prr_1, prr_2, prr_3, prr_4, prr_5, prr_6  - the main parameters which are using for dapa plot 
# (timeseries have to have a time index and appropriate values)
# index has to be in format - datetime
#
# leg_1, leg_2, leg_3, leg_4, leg_5, leg_6 - the name of parameter in legend
#
# n_3 - name of plot (label)
#
# n_4 - name of y - axis
#
# pr_3, pr_4, pr_5 - data scales of data range (pr_3 - from, pr_4 - to, pr_5 - step) 
#
# pr_6 - additional parameter for subtips 
#
# l_p  - the position of legend 

# time_step_1,time_step_2 - time range

#
#
# Author: Evgenii Churiulin, CESR, 15.02.2021
#
# 
#------------------------------------------------------------------------------ 

def plot_6d(ax, prr_1, prr_2, prr_3, prr_4, prr_5, prr_6, 
                leg_1, leg_2, leg_3, leg_4, leg_5, leg_6,                
                na_3, na_4, na_5, date_ind, nst,
                l_p, pr_3, pr_4, pr_5, time_step_1, time_step_2):    
    
    ax.plot(prr_1.index, prr_1, label = leg_1, color = 'blue'  , linestyle = '-'  )
    ax.plot(prr_2.index, prr_2, label = leg_2, color = 'orange', linestyle = '--' )
    ax.plot(prr_3.index, prr_3, label = leg_3, color = 'green' , linestyle = '-.', alpha = 0.4 ) 
    ax.plot(prr_4.index, prr_4, label = leg_4, color = 'red'   , linestyle = ':' , alpha = 0.6 )       
    ax.plot(prr_5.index, prr_5, label = leg_5, color = 'tab:brown' , linestyle = '-.')    
    ax.plot(prr_6.index, prr_6, label = leg_6, color = 'lime'      , linestyle = '-' )    
    
    #ax.set_title(na_3 +'\n\n' + date_ind, color = 'black', fontsize = 14, y = 1.02)
    ax.set_title(na_3 +'\n\n' + 'Station: ' + nst + '    ' + date_ind, color = 'black', fontsize = 14, pad=20)
    ax.set_ylabel(na_4, color = 'black', fontsize = 14, labelpad=20)
    ax.set_xlabel(na_5, color = 'black', fontsize = 14, labelpad=20)
    ax.legend(loc = l_p, frameon=False)
    ax.get_yticks()
    ax.set_yticks(np.arange(pr_3, pr_4, pr_5))
    ax.get_xticks()
    ax.tick_params(axis='y', which ='major',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
    ax.tick_params(axis='y', which ='minor',bottom = True, top = False,
                   left = True, right = True, labelleft ='on', labelright = 'on')
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
    ax.grid(True, which ='major', color = 'k', linestyle = 'solid', alpha = 0.5)  

# end def plot_6d
#------------------------------------------------------------------------------
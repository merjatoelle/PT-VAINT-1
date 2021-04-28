# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:44:51 2021

@author: churiulin
"""

import pandas as pd
import sys


#------------------------------------------------------------------------------
# Subroutine: get_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting timeseries based on 
# GLEAM, EOBS or HYRAS reanalysis data
# 
# Input parameters : iPath - absolute path for data
# Output parameters: ts - timeseries with intersting parameter 
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def get_data(iPath):
    df = pd.read_csv(iPath, skiprows = 0, sep=' ', parse_dates = {'Date':[1,2]},
                     header = None)
    df = df.drop(0, axis = 1)
    # Get indices
    date_index = pd.to_datetime(df['Date'])
    # Create timeseries
    ts = pd.Series(df[3].values, index = date_index, dtype = 'float') 
    return ts

# end Subroutine get_data
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine: v35a_path
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual paths for 
# GLEAM reanalysis data  ---> version 3.5a
# 
# Input parameters : mf_com      - general path for research project
#                    sf_gleam    - name of subfolder for GLEAM data
#                    ssf_a       - name of subsubfolder for GLEAM version
#                    sssf_region - name of subsubsubfolder for GLEAM region
#                    fn_region   - file name of intersting parameter
#             
# Output parameters: E_path      - path for Actual Evaporation (E) data
#                    Ei_path     - path for Interception Loss (Ei) data
#                    Ep_path     - path for Potential Evaporation (Ep) data
#                    Es_path     - path for Snow Sublimation (Es) data
#                    Et_path     - path for Transpiration (Et) data
#                    S_path      - path for Evaporative Stress (S) data 
#                    SMroot_path - path for Root-zone Soil Moisture (SMroot) data
#                    SMsurf_path - path for Surface Soil Moisture (SMsurf) data
#
#
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region):    
    # Filename for v3.5_a parameters
    fn_E      = 'E_'      + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Ei     = 'Ei_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Ep     = 'Ep_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Es     = 'Es_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Et     = 'Et_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_S      = 'S_'      + 'GLEAM_' + fn_region + '_mean.csv'
    fn_SMroot = 'SMroot_' + 'GLEAM_' + fn_region + '_mean.csv'
    fn_SMsurf = 'SMsurf_' + 'GLEAM_' + fn_region + '_mean.csv'      
    
    # Path for v3.5_a parameters
    E_path      = mf_com + sf_gleam + ssf_a + sssf_region + fn_E
    Ei_path     = mf_com + sf_gleam + ssf_a + sssf_region + fn_Ei
    Ep_path     = mf_com + sf_gleam + ssf_a + sssf_region + fn_Ep
    Es_path     = mf_com + sf_gleam + ssf_a + sssf_region + fn_Es
    Et_path     = mf_com + sf_gleam + ssf_a + sssf_region + fn_Et
    S_path      = mf_com + sf_gleam + ssf_a + sssf_region + fn_S
    SMroot_path = mf_com + sf_gleam + ssf_a + sssf_region + fn_SMroot
    SMsurf_path = mf_com + sf_gleam + ssf_a + sssf_region + fn_SMsurf
    
    return E_path, Ei_path, Ep_path, Es_path, Et_path, S_path, SMroot_path, SMsurf_path

# end Subroutine v35a_path
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine: v35b_path
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual paths for 
# GLEAM reanalysis data ---> version 3.5b
# 
# Input parameters : mf_com      - general path for research project
#                    sf_gleam    - name of subfolder for GLEAM data
#                    ssf_a       - name of subsubfolder for GLEAM version
#                    sssf_region - name of subsubsubfolder for GLEAM region
#                    fn_region   - file name of intersting parameter
#             
# Output parameters: E_path      - path for Actual Evaporation (E) data
#                    Ep_path     - path for Potential Evaporation (Ep) data
#                    Es_path     - path for Snow Sublimation (Es) data
#                    Et_path     - path for Transpiration (Et) data
#                    S_path      - path for Evaporative Stress (S) data 
#                    SMroot_path - path for Root-zone Soil Moisture (SMroot) data
#                    SMsurf_path - path for Surface Soil Moisture (SMsurf) data
#
#
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------
def v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region):    
    # Filename for v3.5_b parameters
    fn_E      = 'E_'      + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Ep     = 'Ep_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Es     = 'Es_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_Et     = 'Et_'     + 'GLEAM_' + fn_region + '_mean.csv'
    fn_S      = 'S_'      + 'GLEAM_' + fn_region + '_mean.csv'
    fn_SMroot = 'SMroot_' + 'GLEAM_' + fn_region + '_mean.csv'
    fn_SMsurf = 'SMsurf_' + 'GLEAM_' + fn_region + '_mean.csv'      
    
    # Path for v3.5_a parameters
    E_path      = mf_com + sf_gleam + ssf_b + sssf_region + fn_E
    Ep_path     = mf_com + sf_gleam + ssf_b + sssf_region + fn_Ep
    Es_path     = mf_com + sf_gleam + ssf_b + sssf_region + fn_Es
    Et_path     = mf_com + sf_gleam + ssf_b + sssf_region + fn_Et
    S_path      = mf_com + sf_gleam + ssf_b + sssf_region + fn_S
    SMroot_path = mf_com + sf_gleam + ssf_b + sssf_region + fn_SMroot
    SMsurf_path = mf_com + sf_gleam + ssf_b + sssf_region + fn_SMsurf
    
    return E_path, Ep_path, Es_path, Et_path, S_path, SMroot_path, SMsurf_path

# end Subroutine v35a_path
#------------------------------------------------------------------------------





#------------------------------------------------------------------------------
# Subroutine: gleam_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual data for 
# GLEAM reanalysis data with information about evaporation, transpiration,
# interception, sublimation and soil moisture in the three regions
# 
# Input parameters : main_path   - general path for research project
#                    sf_path     - name of subfolder for GLEAM data
#                    sssf_region - name of subsubsubfolder for GLEAM data region
#                    lversion_a  - logical parameter for version 3.5a        (true or false)
#                    lversion_b  - logical parameter for version 3.5b        (true or false)
#                    lversion_bh - logical parameter for version 3.5bt       (true or false)
#                    lpark       - logical parameter for park region         (true or false)
#                    llinden     - logical parameter for linden region       (true or false)
#                    llindenberg - logical parameter for lindenberg region   (true or false)
#             
# Output parameters: df_GLEAM_v35a  - for version v3.5a
#                    df_GLEAM_v35b  - for version v3.5b
#                    df_GLEAM_v35bt - for version v3.5bt
#
# Data in output dataframe: E      - data for Actual Evaporation (E) data         
#                           Ei     - data for Interception Loss (Ei) data                     
#                           Ep     - data for Potential Evaporation (Ep) data      
#                           Es     - data for Snow Sublimation (Es) data          
#                           Et     - data for Transpiration (Et) data              
#                           S      - data for Evaporative Stress (S) data          
#                           SMroot - data for Root-zone Soil Moisture (SMroot) data 
#                           SMsurf - data for Surface Soil Moisture (SMsurf) data   
# 
# Additional comment: prefix - a - for v3.5a and b for v 3.5b
#  
#  
#
#
# Note: ssf_a, ssf_b - should be changed according to actual folder name
#
# 
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------


def gleam_data(main_path, sf_path, sssf_region, fn_region,
               lversion_a, lversion_b, lversion_bt,
               lpark, llinden, llindenberg):
    # Main path
    mf_com   = main_path
    # Folder name (path)
    sf_gleam = sf_path
    

    # Start programm
    
    #--------------------------------------------------------------------------
    # Section for logical data types
    #--------------------------------------------------------------------------
    
    # Don't change them
    version_a       = True                                                     # version 3.5_a
    version_b       = True                                                     # version 3.5_b
    version_bt      = True                                                     # both version together
    park_area       = True                                                     # park region
    linden_area     = True                                                     # linden region
    lindenberg_area = True                                                     # lindenberg region
    #End of section
    #--------------------------------------------------------------------------
                     
    
    #--------------------------------------------------------------------------
    # Section: Define pahts to actual region and version of model
    #--------------------------------------------------------------------------
    
    if version_a == lversion_a:
        # Name of folder with Version 3.5a - Should be changed for actual name
        ssf_a = 'v3.5_a/'
        
        if park_area == lpark:
            # Get paths 
            E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a, S_path_a, SMroot_path_a, SMsurf_path_a = v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region)
            print('Got data paths for v3.5a - Park region \n')
        elif linden_area == llinden:
            # Get paths
            E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a, S_path_a, SMroot_path_a, SMsurf_path_a = v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region)
            print('Got data paths  for v3.5a  - Linden region \n')        
        elif lindenberg_area == llindenberg:
            # Get paths
            E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a, S_path_a, SMroot_path_a, SMsurf_path_a = v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region)
            print('Got data paths  for v3.5a  - Lindenberg region \n')
        else:
            print('Error: Incorrect format of region for v3.5a \n')
            sys.exit()
    
    elif version_b == lversion_b:
        # Name of folder with Version 3.5b - Should be changed for actual name
        ssf_b = 'v3.5_b/'
        
        if park_area == lpark:
            # Get paths 
            E_path_b, Ep_path_b, Es_path_b, Et_path_b, S_path_b, SMroot_path_b, SMsurf_path_b = v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region)
            print('Got data paths for v3.5b - Park region \n')
        elif linden_area == llinden:
            # Get paths
            E_path_b, Ep_path_b, Es_path_b, Et_path_b, S_path_b, SMroot_path_b, SMsurf_path_b = v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region)
            print('Got data path for v3.5b  - Linden region \n')        
        elif lindenberg_area == llindenberg:
            # Get paths
            E_path_b, Ep_path_b, Es_path_b, Et_path_b, S_path_b, SMroot_path_b, SMsurf_path_b = v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region)
            print('Got data path for v3.5b  - Lindenberg region \n')
        else:
            print('Error: Incorrect format of region for v3.5b \n')
            sys.exit()    
        
    elif version_bt == lversion_bt:
        # Name of folders with Version 3.5a and 3.5b - Should be changed for actual name
        ssf_a = 'v3.5_a/'
        ssf_b = 'v3.5_b/'
        
        if park_area == lpark:
            # Get paths
            E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a, S_path_a, SMroot_path_a, SMsurf_path_a = v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region)
            E_path_b, Ep_path_b, Es_path_b, Et_path_b, S_path_b, SMroot_path_b, SMsurf_path_b = v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region)
            print('Got data paths for v3.5a and v3.5b - Park region \n')
        elif linden_area == llinden:
            # Get paths
            E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a, S_path_a, SMroot_path_a, SMsurf_path_a = v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region)
            E_path_b, Ep_path_b, Es_path_b, Et_path_b, S_path_b, SMroot_path_b, SMsurf_path_b = v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region)
            print('Got data path for v3.5a and v3.5b  - Linden region \n')        
        elif lindenberg_area == llindenberg:
            # Get paths
            E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a, S_path_a, SMroot_path_a, SMsurf_path_a = v35a_path(mf_com, sf_gleam, ssf_a, sssf_region, fn_region)
            E_path_b, Ep_path_b, Es_path_b, Et_path_b, S_path_b, SMroot_path_b, SMsurf_path_b = v35b_path(mf_com, sf_gleam, ssf_b, sssf_region, fn_region)
            print('Got data path for v3.5a and v3.5b  - Lindenberg region \n')
        else:
            print('Error: Incorrect format of region for v3.5a and v3.5b \n')
            sys.exit()       
        
    else:
        print('Error: Incorrect version of GLEAM data \n')
        sys.exit()
        
      
        
    #------------------------------------------------------------------------------
    # Section: Main calculations
    #------------------------------------------------------------------------------
    
    # Data from GLEAM
    if version_a == lversion_a:
        E_a      = get_data(E_path_a)    
        Ei_a     = get_data(Ei_path_a) 
        Ep_a     = get_data(Ep_path_a)    
        Es_a     = get_data(Es_path_a)   
        Et_a     = get_data(Et_path_a)   
        S_a      = get_data(S_path_a) 
        SMroot_a = get_data(SMroot_path_a) 
        SMsurf_a = get_data(SMsurf_path_a) 
       
    elif version_b == lversion_b:
        E_b      = get_data(E_path_b)    
        Ep_b     = get_data(Ep_path_b)    
        Es_b     = get_data(Es_path_b)   
        Et_b     = get_data(Et_path_b)   
        S_b      = get_data(S_path_b) 
        SMroot_b = get_data(SMroot_path_b) 
        SMsurf_b = get_data(SMsurf_path_b)    
    
    elif version_bt == lversion_bt:
        # version 3.5a
        E_a      = get_data(E_path_a)    
        Ei_a     = get_data(Ei_path_a) 
        Ep_a     = get_data(Ep_path_a)    
        Es_a     = get_data(Es_path_a)   
        Et_a     = get_data(Et_path_a)   
        S_a      = get_data(S_path_a) 
        SMroot_a = get_data(SMroot_path_a) 
        SMsurf_a = get_data(SMsurf_path_a)
        # version 3.5b
        E_b      = get_data(E_path_b)    
        Ep_b     = get_data(Ep_path_b)    
        Es_b     = get_data(Es_path_b)   
        Et_b     = get_data(Et_path_b)   
        S_b      = get_data(S_path_b) 
        SMroot_b = get_data(SMroot_path_b) 
        SMsurf_b = get_data(SMsurf_path_b)        
    else:
        print('Error: No data GLEAM \n')
        sys.exit()    

    if version_a == lversion_a:        
        E_a.index = Ei_a.index = Ep_a.index = Es_a.index = Et_a.index = S_a.index = SMroot_a.index = SMsurf_a.index 
        df_GLEAM_v35a = pd.concat([E_a, Ei_a, Ep_a, Es_a, Et_a, S_a, SMroot_a,
                                   SMsurf_a], axis = 1)
        df_GLEAM_v35a.columns = ['E_a', 'Ei_a', 'Ep_a', 'Es_a','Et_a','S_a','SMroot_a','SMsurf_a']
        
        return df_GLEAM_v35a
    
    elif version_b == lversion_b:
        E_b.index = Ep_b.index = Es_b.index = Et_b.index = S_b.index = SMroot_b.index = SMsurf_b.index 
        df_GLEAM_v35b = pd.concat([E_b, Ep_b, Es_b, Et_b, S_b, SMroot_b, SMsurf_b], axis = 1)
        df_GLEAM_v35b.columns = ['E_b', 'Ep_b', 'Es_b','Et_b','S_b','SMroot_b','SMsurf_b']    
        
        return df_GLEAM_v35b
    
    elif version_bt == lversion_bt:
        

        df_GLEAM_v35bt = pd.concat([E_a, E_b, Ei_a, Ep_a, Ep_b, Es_a, Es_b,
                                    Et_a, Et_b, S_a, S_b, SMroot_a, SMroot_b,
                                    SMsurf_a, SMsurf_b], axis = 1)
        
        df_GLEAM_v35bt.columns = ['E_a', 'E_b', 'Ei_a', 'Ep_a', 'Ep_b', 'Es_a','Es_b',
                                  'Et_a','Et_b', 'S_a','S_b', 'SMroot_a','SMroot_b',
                                  'SMsurf_a','SMsurf_b']
   
        return df_GLEAM_v35bt
        
# end Subroutine gleam_data
#------------------------------------------------------------------------------        
    
   

    
#------------------------------------------------------------------------------
# Subroutine: hyras_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual data for 
# HYRAS reanalysis data with information about temperature
# 
# Input parameters : main_path   - general path for research project
#                    sf_path     - name of subfolder for HYRAS data
#                    sssf_region - name of subsubsubfolder for HYRAS data region
#                    lpark       - logical parameter for park region         (true or false)
#                    llinden     - logical parameter for linden region       (true or false)
#                    llindenberg - logical parameter for lindenberg region   (true or false)
#             
# Output parameters: t2m_hyras   - temperature (C)
#
#
# 
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

          
# Temperature
def hyras_data(main_path, sf_path, sssf_region,
                          lpark, llinden, llindenberg):
 
    # Main path
    mf_com   = main_path
    # Folder name (path)
    sf_hyras = sf_path
    
    fn_hyras = 'tas_hyras_mean.csv'
    # Start programm
    
    #--------------------------------------------------------------------------
    # Section for logical data types
    #--------------------------------------------------------------------------
    
    # Don't change them
    park_area       = True                                                     # park region
    linden_area     = True                                                     # linden region
    lindenberg_area = True                                                     # lindenberg region
    #End of section
    #--------------------------------------------------------------------------
                     
    
    #--------------------------------------------------------------------------
    # Section: Define pahts to actual region
    #--------------------------------------------------------------------------
          
    if park_area == lpark:
            # Get path for HYRAS data 
            iPath_hyras = mf_com + sf_hyras + sssf_region + '{}'.format(fn_hyras)
            print('Got HYRAS data paths for Park region \n')
            
    elif linden_area == llinden:
            # Get path for HYRAS data 
            iPath_hyras = mf_com + sf_hyras + sssf_region + '{}'.format(fn_hyras)
            print('Got HYRAS data paths for Linden region \n')  
            
    elif lindenberg_area == llindenberg:
            # Get path for HYRAS data 
            iPath_hyras = mf_com + sf_hyras + sssf_region + '{}'.format(fn_hyras)
            print('Got HYRAS data paths for Lindenberg region \n')
            
    else:
            print('Error: Incorrect region for HYRAS data \n')
            sys.exit()
    


    t2m_hyras = get_data(iPath_hyras) 
    
    return t2m_hyras

# end Subroutine hyras_data
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Subroutine: eobs_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual data for 
# HYRAS reanalysis data with information about temperature
# 
# Input parameters : main_path   - general path for research project
#                    sf_path     - name of subfolder for EOBS data
#                    sssf_region - name of subsubsubfolder for EOBS data region
#                    lpark       - logical parameter for park region         (true or false)
#                    llinden     - logical parameter for linden region       (true or false)
#                    llindenberg - logical parameter for lindenberg region   (true or false)
#             
# Output parameters: t2m_eobs   - temperature (C)
#
#
# 
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 04.03.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------

def eobs_data(main_path, sf_path, sssf_region,
                     lpark, llinden, llindenberg):
    
    # Main path
    mf_com   = main_path
    # Folder name (path)
    sf_eobs = sf_path
    # Filename of EOBS data
    fn_eobs = 'tg_mean.csv'
    
    # Start programm
    #--------------------------------------------------------------------------
    # Section for logical data types
    #--------------------------------------------------------------------------
    
    # Don't change them
    park_area       = True                                                     # park region
    linden_area     = True                                                     # linden region
    lindenberg_area = True                                                     # lindenberg region
    #End of section
    #--------------------------------------------------------------------------
                     
    
    #--------------------------------------------------------------------------
    # Section: Define pahts to actual region
    #--------------------------------------------------------------------------
          
    if park_area == lpark:
            # Get path for HYRAS data 
            iPath_eobs = mf_com + sf_eobs + sssf_region + '{}'.format(fn_eobs)
            print('Got EOBS data paths for Park region \n')
            
    elif linden_area == llinden:
            # Get path for HYRAS data 
            iPath_eobs = mf_com + sf_eobs + sssf_region + '{}'.format(fn_eobs)
            print('Got EOBS data paths for Linden region \n')  
            
    elif lindenberg_area == llindenberg:
            # Get path for HYRAS data 
            iPath_eobs = mf_com + sf_eobs + sssf_region + '{}'.format(fn_eobs)
            print('Got EOBS data paths for Lindenberg region \n')
            
    else:
            print('Error: Incorrect region for EOBS data \n')
            sys.exit()    
    
    t2m_eobs = get_data(iPath_eobs) 
    
    return t2m_eobs    
    
# end Subroutine eobs_data
#------------------------------------------------------------------------------    
    
 






    
 

    


# -*- coding: utf-8 -*-
"""
The reanalysis_data is the program for work wuith HYRAS, E-OBS, GLEAM data.

The progam contains several subroutines:
    get_data    ---> The subroutine needs for getting timeseries based on 
                     GLEAM, EOBS or HYRAS reanalysis data
    v35a_path   ---> The subroutine needs for getting actual paths for 
                     GLEAM 3.5a
    v35b_path   ---> The subroutine needs for getting actual paths for 
                     GLEAM 3.5b
    gleam_data  ---> The subroutine needs for getting actual data for 
                     GLEAM data with information about evaporation,
                     transpiration, interception, sublimation and soil
                     moisture in the three regions
    hyras_data  ---> The subroutine needs for getting actual data for 
                     HYRAS data with information about temperature
    eobs_data   ---> The subroutine needs for getting actual data for 
                     E-OBS data with information about temperature
        
Autors of project: Evgenii Churiulin, Merja Tölle, Center for Enviromental System
                                                   Research (CESR) 

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
import sys
import pandas as pd


#------------------------------------------------------------------------------
# Subroutine: get_data
#------------------------------------------------------------------------------
# The subroutine needs for getting timeseries based on 
# GLEAM, EOBS or HYRAS reanalysis data
# 
# Input parameters : iPath - absolute path for data
# Output parameters: ts - timeseries with intersting parameter 
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
# The subroutine needs for getting actual paths for 
# GLEAM reanalysis data  ---> version 3.5a
# 
# Input parameters : mf_com      - general path for research project
#                    sf_gleam    - name of subfolder for GLEAM data
#                    fn_region   - file name of intersting parameter
#             
# Output parameters: E_path      - path for Actual Evaporation (E) data
#                    Ei_path     - path for Interception Loss (Ei) data
#                    Ep_path     - path for Potential Evaporation (Ep) data
#                    Es_path     - path for Snow Sublimation (Es) data
#                    Et_path     - path for Transpiration (Et) data
#------------------------------------------------------------------------------
def v35a_path(mf_com, sf_gleam, fn_region):    
    # Filename for v3.5_a parameters
    fn_E      = 'E_'      + 'GLEAM_v3.5a_' + fn_region + '_mean.csv'
    fn_Ei     = 'Ei_'     + 'GLEAM_v3.5a_' + fn_region + '_mean.csv'
    fn_Ep     = 'Ep_'     + 'GLEAM_v3.5a_' + fn_region + '_mean.csv'
    fn_Es     = 'Es_'     + 'GLEAM_v3.5a_' + fn_region + '_mean.csv'
    fn_Et     = 'Et_'     + 'GLEAM_v3.5a_' + fn_region + '_mean.csv'
      
    # Path for v3.5_a parameters
    E_path      = mf_com + sf_gleam + fn_E
    Ei_path     = mf_com + sf_gleam + fn_Ei
    Ep_path     = mf_com + sf_gleam + fn_Ep
    Es_path     = mf_com + sf_gleam + fn_Es
    Et_path     = mf_com + sf_gleam + fn_Et
   
    return E_path, Ei_path, Ep_path, Es_path, Et_path
# end Subroutine v35a_path
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine: v35b_path
#------------------------------------------------------------------------------
# The subroutine needs for getting actual paths for 
# GLEAM reanalysis data ---> version 3.5b
# 
# Input parameters : mf_com      - general path for research project
#                    sf_gleam    - name of subfolder for GLEAM data
#                    fn_region   - file name of intersting parameter
#             
# Output parameters: E_path      - path for Actual Evaporation (E) data
#                    Ep_path     - path for Potential Evaporation (Ep) data
#                    Es_path     - path for Snow Sublimation (Es) data
#                    Et_path     - path for Transpiration (Et) data
#------------------------------------------------------------------------------
def v35b_path(mf_com, sf_gleam, fn_region):    
    # Filename for v3.5_b parameters
    fn_E      = 'E_'      + 'GLEAM_v3.5b_' + fn_region + '_mean.csv'
    fn_Ep     = 'Ep_'     + 'GLEAM_v3.5b_' + fn_region + '_mean.csv'
    fn_Es     = 'Es_'     + 'GLEAM_v3.5b_' + fn_region + '_mean.csv'
    fn_Et     = 'Et_'     + 'GLEAM_v3.5b_' + fn_region + '_mean.csv'
       
    # Path for v3.5_a parameters
    E_path      = mf_com + sf_gleam + fn_E
    Ep_path     = mf_com + sf_gleam + fn_Ep
    Es_path     = mf_com + sf_gleam + fn_Es
    Et_path     = mf_com + sf_gleam + fn_Et
    
    return E_path, Ep_path, Es_path, Et_path
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
#                    lversion_a  - logical parameter for version 3.5a        (true or false)
#                    lversion_b  - logical parameter for version 3.5b        (true or false)
#                    lversion_bh - logical parameter for version 3.5bt       (true or false)
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
# 
# Additional comment: prefix - a - for v3.5a and b for v 3.5b
#------------------------------------------------------------------------------
def gleam_data(main_path, sf_path, fn_region,
               lversion_a, lversion_b, lversion_bt):
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
    #End of section
    #--------------------------------------------------------------------------
                         
    #--------------------------------------------------------------------------
    # Section: Define pahts to actual region and version of model
    #--------------------------------------------------------------------------
    
    if version_a == lversion_a:
        E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a = v35a_path(mf_com, sf_gleam, fn_region)
        print('Got data paths  for GLEAM v3.5a. Domain - ' + fn_region + '\n')   
    elif version_b == lversion_b:
        E_path_b, Ep_path_b, Es_path_b, Et_path_b = v35b_path(mf_com, sf_gleam, fn_region)
        print('Got data paths for v3.5b. Domain - ' + fn_region + '\n')           
    elif version_bt == lversion_bt:
        E_path_a, Ei_path_a, Ep_path_a, Es_path_a, Et_path_a = v35a_path(mf_com, sf_gleam, fn_region)
        E_path_b, Ep_path_b, Es_path_b, Et_path_b = v35b_path(mf_com, sf_gleam, fn_region)
        print('Got data paths for v3.5a and v3.5b. Domain - ' + fn_region + '\n')          
    else:
        print('Error: Incorrect domain of GLEAM data \n')
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
    elif version_b == lversion_b:
        E_b      = get_data(E_path_b)    
        Ep_b     = get_data(Ep_path_b)    
        Es_b     = get_data(Es_path_b)   
        Et_b     = get_data(Et_path_b)        
    elif version_bt == lversion_bt:
        # version 3.5a
        E_a      = get_data(E_path_a)    
        Ei_a     = get_data(Ei_path_a) 
        Ep_a     = get_data(Ep_path_a)    
        Es_a     = get_data(Es_path_a)   
        Et_a     = get_data(Et_path_a)   
        # version 3.5b
        E_b      = get_data(E_path_b)    
        Ep_b     = get_data(Ep_path_b)    
        Es_b     = get_data(Es_path_b)   
        Et_b     = get_data(Et_path_b)          
    else:
        print('Error: No data GLEAM \n')
        sys.exit()    

    if version_a == lversion_a:        
        #E_a.index = Ei_a.index = Ep_a.index = Es_a.index = Et_a.index = S_a.index = SMroot_a.index = SMsurf_a.index 
        E_a.index = Ei_a.index = Ep_a.index = Es_a.index = Et_a.index
        df_GLEAM_v35a = pd.concat([E_a, Ei_a, Ep_a, Es_a, Et_a], axis = 1)
        df_GLEAM_v35a.columns = ['E_a', 'Ei_a', 'Ep_a', 'Es_a','Et_a']
        
        return df_GLEAM_v35a
    
    elif version_b == lversion_b:
        E_b.index = Ep_b.index = Es_b.index = Et_b.index
        df_GLEAM_v35b = pd.concat([E_b, Ep_b, Es_b, Et_b], axis = 1)
        df_GLEAM_v35b.columns = ['E_b', 'Ep_b', 'Es_b','Et_b']    
        
        return df_GLEAM_v35b
    
    elif version_bt == lversion_bt:
        df_GLEAM_v35bt = pd.concat([E_a , E_b , Ei_a, Ep_a,
                                    Ep_b, Es_a, Es_b, Et_a, Et_b], axis = 1)        
        df_GLEAM_v35bt.columns = ['E_a' , 'E_b' , 'Ei_a', 'Ep_a', 
                                  'Ep_b', 'Es_a', 'Es_b', 'Et_a', 'Et_b']
   
        return df_GLEAM_v35bt
        
# end Subroutine gleam_data
#------------------------------------------------------------------------------        
   
#------------------------------------------------------------------------------
# Subroutine: hyras_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual data for 
# HYRAS reanalysis data with information about temperature
# 
# Input parameters : main_path - general path for research project
#                    sf_path   - name of subfolder for HYRAS data
#                    param     - list of HYRAS parameters
#                    domain    - research region
#             
# Output parameters: df_hyras   - temperature (C)
#------------------------------------------------------------------------------        
def hyras_data(main_path, sf_path, param, domain):
    hyras_list = []
    for i in range(len(param)):
        iPath_hyras = main_path + sf_path + 'HYRAS_' + param[i] + '_' + domain + '_mean.csv'
        hyras = get_data(iPath_hyras)
        hyras_list.append(hyras)
    df_hyras = pd.concat(hyras_list, axis = 1)    
    df_hyras.columns = [str(i) for i in param]  
    print('Got HYRAS data. Domain: ' + domain + '\n')    
    return df_hyras

# end Subroutine hyras_data
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Subroutine: eobs_data
#------------------------------------------------------------------------------
# The subroutine needs for getting actual data for 
# HYRAS reanalysis data with information about temperature
# 
# Input parameters : main_path   - general path for research project
#                    sf_path     - name of subfolder for EOBS data
#                    domain      - research region        
#             
# Output parameters: t2m_eobs   - temperature (C)
#------------------------------------------------------------------------------
def eobs_data(main_path, sf_path, domain):
    iPath_eobs = main_path + sf_path + 'EOBS_T_2M_' + domain + '_mean.csv'
    eobs = get_data(iPath_eobs)
    df_eobs = eobs.to_frame() 
    df_eobs.columns = [domain]  
    print('Got EOBS data. Domain: ' + domain + '\n')    
    return df_eobs      
# end Subroutine eobs_data
#------------------------------------------------------------------------------    
    





    
 

    


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
# Subroutine: gleam_data
#------------------------------------------------------------------------------
#
# The subroutine needs for getting actual data for 
# GLEAM reanalysis data with information about evaporation, transpiration,
# interception, sublimation and soil moisture in the three regions
# 
# Input parameters : main_path   - general path for research project
#                    sf_path     - name of subfolder for GLEAM data
#             
# Output parameters: df_v35a  - for version v3.5a
#                    df_v35b  - for version v3.5b

#
# Data in output dataframe: E      - data for Actual Evaporation (E) data                           
#                           Ep     - data for Potential Evaporation (Ep) data      
#                           Es     - data for Snow Sublimation (Es) data          
#                           Et     - data for Transpiration (Et) data              
# 
#------------------------------------------------------------------------------
def gleam_data(sf_path, fn_region):
      
    # Get GLEAM paths
    #--------------------------------------------------------------------------
    def get_path(sf_path, fn_region, name_dataset, paremeters):      
        data = []
        for param in paremeters:
            name = f'{param}_{name_dataset}_{fn_region}_mean.csv'
            data.append(sf_path + name)
        return data 
    #--------------------------------------------------------------------------    
                      
    # Actual parameteres of GlEAM datasets   
    param_name = ['E', 'Ep', 'Es', 'Et']
    
    # Define pahts for GLEAM datasets
    gleam35a_path = get_path(sf_path, fn_region, 'GLEAM_v3.5a', param_name)        
    gleam35b_path = get_path(sf_path, fn_region, 'GLEAM_v3.5b', param_name)
    
    # Get data for dataset GLEAM v3.5a
    v35a = []
    for path in gleam35a_path:
        v35a.append(get_data(path))

    # Get data for dataset GLEAM v3.5b
    v35b = []
    for path in gleam35b_path:
        v35b.append(get_data(path))

    # Create dataframe for GLEAM v3.5a data    
    df_v35a = pd.concat(v35a, axis=1)
    df_v35a.columns = ['E', 'Ep', 'Es', 'Et']
        
    # Create dataframe for GLEAM v3.5b data    
    df_v35b = pd.concat(v35b, axis=1)
    df_v35b.columns = ['E', 'Ep', 'Es', 'Et']    
       
    return df_v35a, df_v35b
        

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
def hyras_data(sf_path, domain):
    
    # Types of parameters for analysis (HYRAS)
    parameters = ['T_2M', 'T_MAX', 'T_MIN', 'T_S']
    
    hyras_list = []
    for param in parameters:
        iPath_hyras = f'{sf_path}HYRAS_{param}_{domain}_mean.csv'
        hyras = get_data(iPath_hyras)
        hyras_list.append(hyras)
    df_hyras = pd.concat(hyras_list, axis = 1)    
    df_hyras.columns = [str(i) for i in parameters]  
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
def eobs_data(sf_path, domain):
    iPath_eobs = sf_path + 'EOBS_T_2M_' + domain + '_mean.csv'
    eobs = get_data(iPath_eobs)
    df_eobs = eobs.to_frame() 
    df_eobs.columns = ['T_2M']  
    print('Got EOBS data. Domain: ' + domain + '\n')    
    return df_eobs      
# end Subroutine eobs_data
#------------------------------------------------------------------------------    
    








    
"""
mf_com    = 'C:/Users/Churiulin/Desktop/COSMO_RESULTS/' 
sf_gleam   = mf_com +'REANALYSIS/GLEAM/' 
fn_region   = 'parc'  
lversion_a  = False                                                          
lversion_b  = False     
lversion_bt = True


a,b = gleam_data(sf_gleam, fn_region, lversion_a, lversion_b, lversion_bt) 
"""
    
 

    


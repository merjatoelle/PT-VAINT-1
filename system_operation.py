# -*- coding: utf-8 -*-
"""
@author: churiulin
"""


import os


#------------------------------------------------------------------------------
# Subroutine: dep_clean
#------------------------------------------------------------------------------
#
# The subroutine needs for data clening the last results
#
# 
# Input parameters : exit_path - path for results 
#
#
#
# Author: Evgenii Churiulin, Merja Tölle, Center for Environmental Systems
#                                         Research (CESR) --- 16.02.2021
# email: evgenychur@uni-kassel.de
#
#------------------------------------------------------------------------------
def dep_clean(exit_path):
    # Clear the privios results
    dirs_path_exit = os.listdir(exit_path) 
    for file_cosmo in dirs_path_exit:
        os.remove(exit_path + file_cosmo)
        
# end def dep_clean
#------------------------------------------------------------------------------
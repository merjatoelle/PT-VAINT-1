# Stomatal resistance, photosynthesis and "two-big leaf" algorithms in the regional climate model COSMO-CLM


### Authors:
<p align="justify">
Evgenii Churiulin<sup>1</sup>, Vladimir Kopeikin<sup>2</sup>, Markus Übel<sup>3</sup>, Jürgen Helmert<sup>3</sup>, Jean-Marie Bettems<sup>4</sup>, Merja Helena Tölle<sup>1</sup>

- Center for Environmental Systems Research, University of Kassel, 34117 Kassel, Germany
- Hydrometcenter of Russia, 123242 Moscow, Russia
- German Weather Service, 63067 Offenbach am Main, Germany
- Federal Office of Meteorology and Climatology, Zurich, CH-8058, Switzerland

<em><strong>Correspondence to: Evgenii Churiulin (evgenychur@uni-kassel.de)</strong></em>



![rstom](https://github.com/EvgenyChur/PT-VAINT/blob/main/RSTOM.jpg)

 
## The repository contains:
1. The new module with stomatal resistance and leaf photosyntesis for CCLM<sub>v3.5</sub>
    * [src_phenology.f90][phen]
2. The module with constant PFT parameters and other constants for CCLM<sub>v3.5</sub>
    * [src_data_phenology.f90][data]
3. The postprocessing scipts for work with COSMO-CLM results:
    * [main.sh][main_ini] - postprocessing of COSMO-CLM parameters for verification and analysis 
    * [bonus.sh][bonus] - postprocessing of COSMO-CLM parameters for additional tests, future developments
4. The preprocessing scripts for HYRAS, E-OBS, GLEAM datasets:
    * [EOBS_domain][E_dom] - interpolation of E-OBS data to COSMO-CLM grid
    * [HYRAS_domain][H_dom] - interpolation of HYRAS data to COSMO-CLM grid
    * [GLEAM_domain][GL_dom] - interpolation of GLEAM data to COSMO-CLM grid
    * [EOBS_python][E_py] - preprocessing E-OBS data for CESR_project.py and stat_module.py
    * [HYRAS_python][H_py] - preprocessing HYRAS data for CESR_project.py and stat_module.py
    * [GLEAM_python][GL_pyt] - preprocessing GLEAM data for CESR_project.py and stat_module.py
5. The new ***Python*** project, with statistical and visualization modules:
    * [CESR_project.py][cesr] and [stat_module][main] - the main programms for verification, statistical analysis and visualization of COSMO-CLM results:  
        + [cosmo_data.py][cosmo] - personal module for downloading and preparing COSMO data
        + [fluxnet_data.py][flux] - personal module for downloading and preparing FLUXNET and EURONET data
        + [insitu_data.py][insitu] - personal module for downloading and preparing data from Linden and Lindenberg
        + [reanalysis_data][rean] - personal module for downloading and preparing reanalysis data from E-OBS, HYRAS and GLEAM datasets
        + [system_operation][sys] - personal module with a system functions for cleaning data
        + [vis_module][vis] - personal module for data visualization
        + [stat_functions][stat] - personal module for work with statistical analysis
    * [cartopy_map][cart] - personal script for figure 1a

## Author contributions:
Conceptualization, project administration and supervision: MT. Investigation and methodology: MT, JH, J-MB, VK, MU, US, EC. Data curation: MT, EC. Validation: MT, JH, J-MB, VK, MU, EV. Writing – original draft: EC. Writing, review and editing: EC, MT. All authors reviewed and approved the final version of the paper.  

## Competing interests:   
The authors declare that they have no conflict of interest. 
  
## Financial support:
This research was funded by the German Research Foundation (DFG) through grant number 401857120  
  
 
  
[cesr]: https://github.com/EvgenyChur/PT-VAINT/blob/main/CESR_project.py  
[main]: https://github.com/EvgenyChur/PT-VAINT/blob/main/stat_module.py  
[vis]: https://github.com/EvgenyChur/PT-VAINT/blob/main/vis_module.py
[sys]: https://github.com/EvgenyChur/PT-VAINT/blob/main/system_operation.py
[stat]: https://github.com/EvgenyChur/PT-VAINT/blob/main/stat_functions.py
[flux]: https://github.com/EvgenyChur/PT-VAINT/blob/main/fluxnet_data.py
[insitu]: https://github.com/EvgenyChur/PT-VAINT/blob/main/insitu_data.py
[rean]: https://github.com/EvgenyChur/PT-VAINT/blob/main/reanalysis_data.py  
[cosmo]: https://github.com/EvgenyChur/PT-VAINT/blob/main/cosmo_data.py
[main_ini]: https://github.com/EvgenyChur/PT-VAINT/blob/main/main_ini.sh
[bonus]: https://github.com/EvgenyChur/PT-VAINT/blob/main/bonus_ini.sh
[E_dom]: https://github.com/EvgenyChur/PT-VAINT/blob/main/EOBS_domain.sh
[H_dom]: https://github.com/EvgenyChur/PT-VAINT/blob/main/HYRAS_domain.sh
[GL_dom]: https://github.com/EvgenyChur/PT-VAINT/blob/main/GLEAM_domain.sh  
[E_py]: https://github.com/EvgenyChur/PT-VAINT/blob/main/EOBS_python.sh
[H_py]: https://github.com/EvgenyChur/PT-VAINT/blob/main/HYRAS_python.sh
[GL_pyt]: https://github.com/EvgenyChur/PT-VAINT/blob/main/GLEAM_python.sh
[data]: https://github.com/EvgenyChur/PT-VAINT/blob/main/data_phenology.f90
[phen]: https://github.com/EvgenyChur/PT-VAINT/blob/main/src_phenology.f90
[cart]: https://github.com/EvgenyChur/PT-VAINT/blob/main/cartopy_map.py


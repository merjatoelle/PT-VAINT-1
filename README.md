# A new stomatal resistance, photosynthesis and "two-big leaf" algorithms in the regional climate model COSMO-CLM


### Authors:
<p align="justify">
Evgenii Churiulin<sup>1</sup>, Vladimir Kopeikin<sup>2</sup>, Markus Übel<sup>3</sup>, Jürgen Helmert<sup>3</sup>, Jean M. Bettems<sup>4</sup>, Merja H. Tölle<sup>1</sup>

- Center for Environmental Systems Research, University of Kassel, 34117 Kassel, Germany
- Hydrometcenter of Russia, 123242 Moscow, Russia
- German Weather Service, 63067 Offenbach am Main, Germany
- Federal Office of Meteorology and Climatology, Zurich, CH-8058, Switzerland

<em><strong>Correspondence to: Evgenii Churiulin (evgenychur@uni-kassel.de)</strong></em>
</p>

## The repository description:

<p align="justify">
  Climatic changes with warmer temperatures require the need to improve the simplified vegetation scheme of the regional climate model COSMO-CLM, which is not capable of modelling complex processes which depend on temperature, water availability, and day length. Thus, we have implemented the physically based Ball-Berry approach coupled with photosynthesis processes based on Farquhar and Collatz models for C<sub>3</sub> and C<sub>4</sub> plants in the regional climate model COSMO-CLM (CCLM v 5.16). The implementation of the new algorithms includes the replacement of the “one-big leaf” approach by a “two-big leaf” one. We performed single column simulations with COSMO-CLM over three observational sites with C<sub>3</sub> grass plants in Germany for the period from 2010 to 2015 (Parc, Linden and Lindenberg domain). Hereby, we tested three alternative formulations of the new algorithms against a reference simulation (<strong>CCLM<sub>ref</sub></strong>) with no changes. The first formulation (<strong>CCLM<sub>v3.5<sub></strong>) adapts the algorithms for stomatal resistance from the Community Land Model (CLM v3.5), which depend on leaf photosynthesis, CO<sub>2</sub> partial and vapor pressure and maximum stomatal resistance. The second one (<strong>CCLM<sub>v4.5</sub></strong>) includes a soil water stress function as in CLM v4.5. The third one (<strong>CCLM<sub>v4.5e</sub></strong>) is similar to CCLM<sub>v4.5</sub>, but with adapted equations for dry leaf calculations. The results revealed major differences in the annual cycle of stomatal resistance compared to the original algorithm (CCLM<sub>ref</sub>) of the reference simulation. The biggest changes in stomatal resistance are observed from October to April when stomata are closed while summer values are generally less than control values that come closer to measured values. Furthermore, changes in the stomatal resistance algorithms have improved the accuracy of calculated transpiration rate and total evapotranspiration. The results indicate that changes in stomatal resistance and photosynthesis algorithms can improve the accuracy of other parameters of the COSMO-CLM model by comparing them with FLUXNET data, meteorological observations at the sites, and GLEAM datasets.
</p>

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


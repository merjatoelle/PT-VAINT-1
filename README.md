# A new stomatal resistance, photosynthesis and "two-big leaf" algorithms in the regional climate model COSMO-CLM

<p align="justify">
  Climatic changes with warmer temperatures require the need to improve the simplified vegetation scheme of the regional climate model COSMO-CLM, which is not capable of modelling complex processes which depend on temperature, water availability, and day length. Thus, we have implemented the physically based Ball-Berry approach coupled with photosynthesis processes based on Farquhar and Collatz models for C<sub>3</sub> and C<sub>4</sub> plants in the regional climate model COSMO-CLM (CCLM v 5.16). The implementation of the new algorithms includes the replacement of the “one-big leaf” approach by a “two-big leaf” one. We performed single column simulations with COSMO-CLM over three observational sites with C<sub>3</sub> grass plants in Germany for the period from 2010 to 2015 (Parc, Linden and Lindenberg domain). Hereby, we tested three alternative formulations of the new algorithms against a reference simulation (<strong>CCLM<sub>ref</sub></strong>) with no changes. The first formulation (<strong>CCLM<sub>v3.5<sub></strong>) adapts the algorithms for stomatal resistance from the Community Land Model (CLM v3.5), which depend on leaf photosynthesis, CO<sub>2</sub> partial and vapor pressure and maximum stomatal resistance. The second one (<strong>CCLM<sub>v4.5</sub></strong>) includes a soil water stress function as in CLM v4.5. The third one (<strong>CCLM<sub>v4.5e</sub></strong>) is similar to CCLM<sub>v4.5</sub>, but with adapted equations for dry leaf calculations. The results revealed major differences in the annual cycle of stomatal resistance compared to the original algorithm (CCLM<sub>ref</sub>) of the reference simulation. The biggest changes in stomatal resistance are observed from October to April when stomata are closed while summer values are generally less than control values that come closer to measured values. Furthermore, changes in the stomatal resistance algorithms have improved the accuracy of calculated transpiration rate and total evapotranspiration. The results indicate that changes in stomatal resistance and photosynthesis algorithms can improve the accuracy of other parameters of the COSMO-CLM model by comparing them with FLUXNET data, meteorological observations at the sites, and GLEAM datasets.
</p>

![rstom](https://github.com/EvgenyChur/PT-VAINT/blob/main/RSTOM.jpg)

  
## The repository contains:
1. The new module with stomatal resistance and leaf photosyntesis for CCLM<sub>v3.5</sub> --> src_phenology.F90
2. The module with constant PFT parameters and other constants for CCLM<sub>v3.5</sub> --> data_phenology.F90
3. The two scipts for work with COSMO-CLM results:
    * main.sh
    * bonus.sh
   

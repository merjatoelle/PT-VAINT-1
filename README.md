#A new stomatal resistance, photosynthesis and "two-big leaf" algorithms in the regional climate model COSMO-CLM

<p align="justify">
  Climatic changes with warmer temperatures require the need to improve the simplified vegetation scheme of the regional climate model COSMO-CLM, which is not capable of modelling complex processes which depend on temperature, water availability, and day length. Thus, we have implemented the physically based Ball-Berry approach coupled with photosynthesis processes based on Farquhar and Collatz models for C^3 and C4 plants in the regional climate model COSMO-CLM (CCLM v 5.16). The implementation of the new algorithms includes the replacement of the “one-big leaf” approach by a “two-big leaf” one. We performed single column simulations with COSMO-CLM over three observational sites with C3 grass plants in Germany for the period from 2010 to 2015 (Parc, Linden and Lindenberg domain). Hereby, we tested three alternative formulations of the new algorithms against a reference simulation (CCLMref) with no changes. The first formulation (CCLM3.5) adapts the algorithms for stomatal resistance from the Community Land Model (CLM v3.5), which depend on leaf photosynthesis, CO2 partial and vapor pressure and maximum stomatal resistance. The second one (CCLM4.5) includes a soil water stress function as in CLM v4.5. The third one (CCLM4.5e) is similar to CCLM4.5, but with adapted equations for dry leaf calculations. The results revealed major differences in the annual cycle of stomatal resistance compared to the original algorithm (CCLMref) of the reference simulation. The biggest changes in stomatal resistance are observed from October to April when stomata are closed while summer values are generally less than control values that come closer to measured values. Furthermore, changes in the stomatal resistance algorithms have improved the accuracy of calculated transpiration rate and total evapotranspiration. The results indicate that changes in stomatal resistance and photosynthesis algorithms can improve the accuracy of other parameters of the COSMO-CLM model by comparing them with FLUXNET data, meteorological observations at the sites, and GLEAM datasets.
</p>

The repository contains:
1. The new module with stomatal resistance and leaf photosyntesis --> src_phenology.F90
2. The module with constant PFT parameters and other constants --> data_phenology.F90
3. 

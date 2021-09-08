!+ Data module for variables concerned with the FLake Model
!------------------------------------------------------------------------------

MODULE data_phenology

!------------------------------------------------------------------------------
!
! Description:
!  This module contains common definitions, variables and constants for the
!  photosynthesis model. These are:
!
!  - general constants for vegetation and photosyntesis:
!
!  - pft parameter:
!
! Center for Environmental Systems Research, 2020 - 2022
! Evgeny Churiulin, Merja Toelle, Jürgen Helmert, Jean-Marie Bettems
! phone:  +49(170)261-51-04
! email:  evgenychur@uni-kassel.de, merja.toelle@uni-kassel.de,
!         Juergen.Helmert@dwd.de Jean-Marie.Bettems@meteoswiss.ch
!
! Acknowledge: Vladimir Kopeykin
!
! Current Code Owner: DWD, Juergen Helmert
!  phone:  +49  69  8062 2704
!  fax:    +49  69  8062 3721
!  email:  Juergen.Helmert@dwd.de
!
!
! History:
! Version    Date       Name
! ---------- ---------- ----
! 5.15       2021/01/12 Evgenii Churiulin
!  Initial release
!
! Code Description:
! Language: Fortran 90.
! Software Standards: "European Standards for Writing and
! Documenting Exchangeable Fortran 90 Code".
!==============================================================================

! Modules used:

USE data_parameters, ONLY :   &
    ireals,    & ! KIND-type parameter for real variables
    iintegers    ! KIND-type parameter for standard integer variables

!==============================================================================

IMPLICIT NONE
!==============================================================================
!
! Declarations
!
!
! Constants are for leaf boundary layer resistance
REAL (KIND = ireals), PARAMETER ::   &
    TTC_CAN = 0.01                     ! The turbulent transfer coefficient
                                       ! between the canopy surface and canopy air                 [m s**-0.5]


! Constants are for the available water in soil
REAL (KIND = ireals), PARAMETER ::   &
    VEG_PAR = 1.0                      ! The vegetation dependent PARAMETER

! Constants are for Vcmax25 calculations
REAL (KIND = ireals), PARAMETER ::   &
    ALPHA_R_25 = 60.0,               & ! The specific active of Rubisco                            [umol/gRubisco/s]
    ALPHA_VMAX = 2.4,                & ! The value of temperature sensitive parameter
    F_NR       = 7.16                  ! The mass ration of total Rubisco molecular mass to
                                       ! nitrogen in Rubisco                                       [g Rubisco g^-1 N in Rubisco]

! Constants are for stomatal resistance calculations
REAL (KIND = ireals), PARAMETER ::   &
    RSMAX0   = 2.e4,              & ! The maximum stomatal resistance                           [    s/m    ]
    GLMIN    = 2000.0                  ! The minimum leaf conductance                              [umol/m**2/s]
    !GLMIN    = 10000.0
! Constants are for the Michaelis-Menten constants calculations
REAL (KIND = ireals), PARAMETER ::   &
    K_C25    = 30.0,                 & ! The concentration values of CO2 at 25 °C                  [Pa]
    ALPHA_KC = 2.1,                  & ! The temperature sensitive parameter for CO2
    K_O25    = 30000.0,              & ! The concentration values of  O2 at 25 °C                  [Pa]
    ALPHA_KO = 1.2                     ! The temperature sensitive parameter for  O2


! Concentration of O2 and CO2 in air
REAL (KIND = ireals), PARAMETER ::      &
    CONST_P_STD = 101325.0,             & ! The standart pressure (Have to be changed on COSMO data)
    CON_O2  = 0.2 * CONST_P_STD,        & ! The O2 concentration                                       [Pa]
    CON_CO2 = 355 * 1.e-6 * CONST_P_STD   ! The CO2 concentration                                      [Pa]

! Constants for Section 5 ---> SUBROUTINE CNMResp
REAL (KIND = ireals), PARAMETER ::   &

    B_RATE = 2.525e-6,               & ! base rate for maintenance respiration
                                       ! (M. Ryan, 1991. Effects of climate change on plant respiration.)
    Q_10 = 2.0                         ! temperature dependence



! 2. Parameters for the pft types
! -------------------------------------------------------------------
! Constants for different types of pft:

INTEGER  (KIND=iintegers), PARAMETER ::  &
    pft_type     = 2,       & ! consist information about different PFT (pft_type 1 - is resopnsible for C3 grass,
    !                                                                    pft_type 2 - is responsible for C4 grass)
    param        = 48,      & ! consist information about different parameters of each PFT types

    ! Parameters values for Table 1.
    R_ZOM        = 1,       & ! param 01 - is responsible for parameter - z0mr;
    R_DISP       = 2,       & ! param 02 - is responsible for parameter - displar;
    D_LEAF       = 3,       & ! param 03 - is responsible for parameter - dleaf;
    C3_PSN       = 4,       & ! param 04 - is responsible for parameter - c3psn;
    V_CMX25      = 5,       & ! param 05 - is responsible for parameter - vcmx25
    MP           = 6,       & ! param 06 - is responsible for parameter - mp;
    ALPHA        = 7,       & ! param 07 - is responsible for parameter - qe25;
    ALPHA_vl     = 8,       & ! param 08 - is responsible for parameter - rhol_vis;
    ALPHA_nl     = 9,       & ! param 09 - is responsible for parameter - rhol_nir;
    ALPHA_vs     = 10,      & ! param 10 - is responsible for parameter - rhos_vis;
    ALPHA_ns     = 11,      & ! param 11 - is responsible for parameter - rhos_nir;
    TETA_vl      = 12,      & ! param 12 - is responsible for parameter - taul_vis;
    TETA_nl      = 13,      & ! param 13 - is responsible for parameter - taul_nir;
    TETA_vs      = 14,      & ! param 14 - is responsible for parameter - taus_vis;
    TETA_ns      = 15,      & ! param 15 - is responsible for parameter - taus_nir;
    X_l          = 16,      & ! param 16 - is responsible for parameter - xl;
    ROOTA_PAR    = 17,      & ! param 17 - is responsible for parameter - roota_par;
    ROOTB_PAR    = 18,      & ! param 18 - is responsible for parameter - rootb_par;
    SLA_o        = 19,      & ! param 19 - is responsible for parameter - slasun;
    SLA_m        = 20,      & ! param 20 - is responsible for parameter - dsladlai;
    CN_L         = 21,      & ! param 21 - is responsible for parameter - leafcn;
    F_LNR        = 22,      & ! param 22 - is responsible for parameter - flnr;
    PSI_o        = 23,      & ! param 23 - is responsible for parameter - smpso;
    PSI_c        = 24,      & ! param 24 - is responsible for parameter - smpsc;
    F_N          = 25,      & ! param 25 - is responsible for parameter - fnitr;
    WOODY        = 26,      & ! param 26 - is responsible for parameter - woody;
    LF_LIT_CN    = 27,      & ! param 27 - is responsible for parameter - lflitcn;
    F_ROOT_CN    = 28,      & ! param 28 - is responsible for parameter - frootcn;
    LIVEWD_CN    = 29,      & ! param 29 - is responsible for parameter - livewdcn;
    DEADWD_CN    = 30,      & ! param 30 - is responsible for parameter - deadwdcn;
    F_ROOT_LEAF  = 31,      & ! param 31 - is responsible for parameter - froot_leaf;
    STEM_LEAF    = 32,      & ! param 32 - is responsible for parameter - stem_leaf;
    C_ROOT_STEM  = 33,      & ! param 33 - is responsible for parameter - croot_stem;
    F_LIVE_WD    = 34,      & ! param 34 - is responsible for parameter - flivewd;
    F_CUR        = 35,      & ! param 35 - is responsible for parameter - fcur;
    LF_FLAB      = 36,      & ! param 36 - is responsible for parameter - lf_flab;
    LF_FCEL      = 37,      & ! param 37 - is responsible for parameter - lf_fcel;
    LF_FLIG      = 38,      & ! param 38 - is responsible for parameter - lf_flig;
    FR_FLAB      = 39,      & ! param 39 - is responsible for parameter - fr_flab;
    FR_FCEL      = 40,      & ! param 40 - is responsible for parameter - fr_fcel;
    FR_FLIG      = 41,      & ! param 41 - is responsible for parameter - fr_flig;
    DW_FCEL      = 42,      & ! param 42 - is responsible for parameter - dw_fce;
    DW_FLIG      = 43,      & ! param 43 - is responsible for parameter - dw_flig;
    LEAF_LONG    = 44,      & ! param 44 - is responsible for parameter - leaf_long;
    EVERGREEN    = 45,      & ! param 45 - is responsible for parameter - evergreen;
    STRESS_DECID = 46,      & ! param 46 - is responsible for parameter - stress_decid;
    SEASON_DECID = 47,      & ! param 47 - is responsible for parameter - season_decid;
    RESIST       = 48         ! param 48 - is responsible for parameter - resist;

    ! Table 1: pft_aero_prop - Plant functional type aerodynamic parameters
    !                          C3_grass      C4_grass
    REAL (KIND=ireals), DIMENSION(pft_type, param), PARAMETER :: &
        pft_CN_par = (/(/      0.120 ,       0.120    /),       & ! 1 The ratio of momentum roughness length to canopy top height
                       (/      0.68  ,       0.68     /),       & ! 2 The ratio of displacement height to canopy top height
                       (/      0.04  ,       0.04     /),       & ! 3 The characteristic dimension of the leaves in the direction of wind flow
                       (/      1.0   ,       0.0      /),       & ! 4 The photosynthetic pathway: 0. = c4, 1. = c3
                       (/     52.0   ,      52.0      /),       & ! 5 The max rate of carboxylation at 25C                                        [     umol CO2/m**2/s    ]
                       (/      9.0   ,       5.0      /),       & ! 6 The slope of conductance-to-photosynthesis relationship
                       (/      0.06  ,       0.04     /),       & ! 7 The quantum efficiency  at 25C                                              [μmol CO2 per μmol photon]
                       (/      0.11  ,       0.11     /),       & ! 8 The weighted combination of the leaf reflectances                           [           VIS          ]
                       (/      0.35  ,       0.35     /),       & ! 9 The weighted combination of the leaf reflectances                           [           NIR          ]
                       (/      0.31  ,       0.31     /),       & ! 10 The weighted combination of the stem reflectances                           [           VIS          ]
                       (/      0.53  ,       0.53     /),       & ! 11 The weighted combination of the stem reflectances                           [           NIR          ]
                       (/      0.05  ,       0.05     /),       & ! 12 The weighted combination of the leaf transmittances                         [           VIS          ]
                       (/      0.34  ,       0.34     /),       & ! 13 The weighted combination of the leaf transmittances                         [           NIR          ]
                       (/      0.120 ,       0.120    /),       & ! 14 The weighted combination of the stem transmittances                         [           VIS          ]
                       (/      0.250 ,       0.250    /),       & ! 15 The weighted combination of the stem transmittances                         [           NIR          ]
                       (/     -0.30  ,      -0.30     /),       & ! 16 The departure of leaf angles from a random distribution equals
                                                                  ! +1 for horizontal, 0 for random , and –1 for vertical
                       (/     11.0   ,      11.0      /),       & ! 17 The rooting distribution parameter                                          [           1/m          ]
                       (/      2.0   ,       2.0      /),       & ! 18 The rooting distribution parameter                                          [           1/m          ]
                       (/      0.030 ,       0.030    /),       & ! 19 The value for SLA at the top of canopy                                      [   m^2 leaf area g^-1 C ]
                       (/      0.0   ,       0.0      /),       & ! 20 The linear slope coefficient
                       (/     25.0   ,      25.0      /),       & ! 21 The leaf carbon to nitrogen ratio (leaf C:N)                                [          gC/gN         ]
                       (/      0.09  ,       0.09     /),       & ! 22 The fraction of leaf nitrogen in Rubisco                                    [         no units       ]
                       (/     -0.74e5,      -0.74e5   /),       & ! 23 The soil water potential when stomata fully open                            [            mm          ]
                       (/     -2.75e5,      -2.75e5   /),       & ! 24 The soil water potential when stomata fully close                           [            mm          ]
                       (/      0.61  ,       0.64     /),       & ! 25 The nitrogen availability factor                                            [          m2 g^-1 C     ]
                       (/      0.0   ,       0.0      /),       & ! 26 binary flag for woody lifeform: 1. = woody, 0. = not woody
                       (/     50.0   ,      50.0      /),       & ! 27 The leaf litter C:N                                                         [           cG/gN        ]
                       (/     42.0   ,      42.0      /),       & ! 28 The fine root C:N                                                           [           gC/gN        ]
                       (/      0.0   ,       0.0      /),       & ! 29 The live wood (phloem and ray parenchyma) C:N                               [           gC/gN        ]
                       (/      0.0   ,       0.0      /),       & ! 30 The dead wood (xylem and heartwood) C:N                                     [           gC/gN        ]
                       (/      3.0   ,       3.0      /),       & ! 31 The allocation parameter: new fine root C per new leaf C                    [           gC/gC        ]
                       (/      0.0   ,       0.0      /),       & ! 32 The allocation parameter: new stem c per new leaf C                         [           gC/gC        ]
                       (/      0.0   ,       0.0      /),       & ! 33 The allocation parameter: new coarse root C per new stem C                  [           gC/gC        ]
                       (/      0.0   ,       0.0      /),       & ! 34 The allocation parameter: fraction of new wood that is live                 [          no units      ]
                       (/      0.5   ,       0.5      /),       & ! 35 The allocation parameter: fraction of allocation that goes
                                                                  ! to currently displayed growth, remainder to storage
                       (/      0.25  ,       0.25     /),       & ! 36 The leaf litter labile fraction
                       (/      0.50  ,       0.50     /),       & ! 37 The leaf litter cellulose fraction
                       (/      0.25  ,       0.25     /),       & ! 38 The leaf litter lignin fraction
                       (/      0.25  ,       0.25     /),       & ! 39 The fine root litter labile fraction
                       (/      0.50  ,       0.50     /),       & ! 40 The fine root litter cellulose fraction
                       (/      0.25  ,       0.25     /),       & ! 41 The fine root litter lignin fraction
                       (/      0.75  ,       0.75     /),       & ! 42 The dead wood cellulose fraction
                       (/      0.25  ,       0.25     /),       & ! 43 The dead wood lignin fraction
                       (/      1.0   ,       1.0      /),       & ! 44 The leaf longevity (yrs)
                       (/      0.0   ,       0.0      /),       & ! 45 binary flag for evergreen leaf habit (0 or 1)
                       (/      1.0   ,       1.0      /),       & ! 46 binary flag for stress-deciduous leaf habit (0 or 1)
                       (/      0.0   ,       0.0      /),       & ! 47 binary flag for seasonal-deciduous leaf habit (0 or 1)
                       (/      0.12  ,       0.12     /)/)        ! 48 fire resistance index (unitless)





!LOGICAL, PARAMETER :: &
  !tree   = .FALSE.    & ! tree pft
  !nort_hem = .TRUE.     ! map of nothern hemispere coordinates


!==============================================================================

END MODULE data_phenology


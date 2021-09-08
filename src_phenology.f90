!+ Source module  "src_phenology"
!------------------------------------------------------------------------------

MODULE src_phenology

!------------------------------------------------------------------------------
!! Description:
! This module contains algorithm for calculation photosyntesis and stomatal resistance
! The module "src_phenology" performs calculation related to the parametrization
! of vegetation process. It contains the one soubroutine photosintes which comprise
! the photosynthecic proccessies in C3 and C4 plants
!
!
!
!
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
!==============================================================================!

!
! Declarations:
!
! Modules used:

USE data_parameters, ONLY :     &
    ireals,                     & ! KIND-type parameter for real variables
    iintegers                     ! KIND-type parameter for standard integer variables
! end of data_parameters
!------------------------------------------------------------------------------

USE data_constants, ONLY :      &
! 1. mathematical constants
! -------------------------
    pi,                         & ! circle constant
    R_to_D,                     & ! convert radian to degree
    D_to_R,                     & ! convert degree to radian

! 2. physical constants and related variables
! -------------------------------------------
    t0_melt,                    & !Freezing temperature of fresh water                          [   K       ]
    g,                          & ! acceleration of gravity                                     [m/s**2     ]
    sigma,                      & ! Stefan-Boltzmann constant                                   [W/m**2/K**4]
    rgas,                       & ! Universal gas constant                                      [J/K/kmol   ]
    r_d,                        & ! Dry air gas constant                                        [J/K/kg     ]
    r_v,                        & ! Water vapor gas constant                                    [J/K/kg     ]
    rdv,                        & ! r_d / r_v
    o_m_rdv,                    & ! 1 - r_d/r_v
    rvd_m_o,                    & ! r_v/r_d -1
    rho_w,                      & ! Density of liquid water                                     [kg/m**3    ]
    rho_ice,                    & ! Density of ice                                              [kg/m**3    ]
    lh_v,                       & ! latent heat of vapourization
    lh_f,                       & ! latent heat of fusion
    lh_s                          ! latent heat of sublimation

! end of data_constants
!------------------------------------------------------------------------------

USE data_phenology, ONLY :      &
    TTC_CAN,                    & ! The turbulent transfer coefficient
    VEG_PAR,                    & ! The vegetation dependent PARAMETER
    ALPHA_R_25,                 & ! The specific active of Rubisco                              [μmol CO2 g^-1 Rubisco s^-1]
    ALPHA_VMAX,                 & ! The value of temperature sensitive parameter
    F_NR,                       & ! The mass ration of total Rubisco molecular mass to
                                  ! nitrogen in Rubisco                                         [g Rubisco g^-1 N in Rubisco]
    RSMAX0,                     & ! The maximum stomatal resistance                             [s/m]
    GLMIN,                      & ! The minimum leaf conductance                                [umol/m**2/s]
    K_C25,                      & ! The concentration values of CO2 at 25 °C                    [Pa]
    ALPHA_KC,                   & ! The temperature sensitive parameter for CO2
    K_O25,                      & ! The concentration values of  O2 at 25 °C                    [Pa]
    ALPHA_KO,                   & ! The temperature sensitive parameter for  O2
    CON_O2,                     & ! The O2 concentration based on STD_PRESS                     [Pa]
    CON_CO2,                    & ! The CO2 concentration based on STD_PRESS                    [Pa]
    pft_type,                   & ! Index of PFT parameters for PFT types (string)              []
    param,                      & ! Index of PFT parameters in PFT tables (column)              []
    MP,                         & ! The slope of conductance-to-photosynthesis relationship     []
    ALPHA,                      & ! The quantum efficiency                                      [μmol CO2 per μmol photon]
    CN_L,                       & ! The leaf carbon to nitrogen ratio                           [g C g^-1 N]
    F_LNR,                      & ! The fraction of leaf nitrogen in Rubisco                    [g N in Rubisco g^-1 N]
    F_N,                        & ! The nitrogen availability factor                            [m2 g^-1 C]
    SLA_o,                      & ! The value for SLA at the top of canopy                      [m^2 leaf area g^-1 C]
    SLA_m,                      & ! The linear slope coefficient
    PSI_o,                      & ! The soil water potential when stomata fully open            [mm]
    PSI_c,                      & ! The soil water potential when stomata fully close           [mm]
    X_l,                        & ! The departure of leaf angles from a random distribution
    R_ZOM,                      & ! The ratio of momentum roughness length to canopy top height
    R_DISP,                     & ! The ratio of displacement height to canopy top height
    D_LEAF,                     & ! The leaves dimension
    WOODY,                      & ! The binary flag for woody lifeform: 1. = woody, 0. = not woody
    pft_CN_par                    ! Plant functional type (PFT) photosynthetic parameters


! end of data_phenology
!------------------------------------------------------------------------------

!==============================================================================

IMPLICIT NONE

!------------------------------------------------------------------------------
! Declarations
!------------------------------------------------------------------------------

CONTAINS

!==============================================================================
!+ Computation of the first part of the soil parameterization scheme
!------------------------------------------------------------------------------


    SUBROUTINE get_stomatal_grid(ie, je, istarts, iends, jstarts, jends, plant_types, pft)

        ! Modules used:

        USE data_fields, ONLY :        &
            soiltyp,                   & ! type of the soil (keys 0-9)
            llandmask                    ! landpoint mask

        ! end of data_fields
        !------------------------------------------------------------------------------


        IMPLICIT NONE
        INTEGER (KIND=iintegers), INTENT (IN) ::    &
            ie, je,                                 & ! dimensions of the fields
            istarts, iends, jstarts, jends            ! start and end-indices of the computation

        INTEGER (KIND=iintegers), INTENT(INOUT)  :: &
            plant_types(ie,je),                     & ! The type of plants. Can be 1 (C3_grass)
                                                      ! or 2 (C4_grass)
            pft(ie,je)                                ! The type of PFT needs for defining
                                                      ! constatn values from module data_phenology


        !==============================================================================
        ! Local parameters:
        ! -----------------------------------------------------------------------------
        INTEGER (KIND=iintegers)             ::    &
            i,                                     & ! loop index in x-direction
            j                                        ! loop index in y-direction

        INTEGER (KIND=iintegers), PARAMETER ::     &
            C3_grass = 1,                          & ! index of column in pft_CN_par and pft_CN_par tables
            C4_grass = 2                             ! index of column in pft_CN_par and pft_CN_par tables

        !- End of header
        !==============================================================================

        !------------------------------------------------------------------------------
        ! Begin subroutine: get_stomatal_grid
        !------------------------------------------------------------------------------

        !------------------------------------------------------------------------------
        ! Section 1: Initialisation of PFT grid parameters
        !------------------------------------------------------------------------------

        DO j = jstarts, jends
            DO i = istarts, iends
                IF(llandmask(i,j)) THEN        ! for land-points only
                    plant_types(i,j) = 1       ! fill in all PFT grid points actual one type PFT values
                ENDIF
            ENDDO
        ENDDO

        DO j = jstarts, jends
            DO i = istarts, iends
                IF(llandmask(i,j)) THEN        ! for land-points only
                    ! Type of PFTs and PFTs constants
                    IF (plant_types(i,j) == 1) THEN
                        pft(i,j) = C3_grass
                    ELSE
                        pft(i,j) = C4_grass
                    ENDIF
                ENDIF
            ENDDO
        ENDDO

        RETURN
    !==============================================================================
    END SUBROUTINE get_stomatal_grid



    SUBROUTINE get_sun_data(ie, je, istarts, iends, jstarts, jends, dt, ntstep,&
                            day_length, f_dyl)

        ! Modules used:
        USE utilities, ONLY: &
            get_utc_date   ! subroutine for calculating the actual day

        ! end of utilities
        !-----------------------------------------------------------------------

        USE data_io, ONLY:  &
            ydate_ini      ! start of the forecast

        ! end of data_io
        !-----------------------------------------------------------------------

        USE data_runcontrol, ONLY:  &
            itype_calendar            ! for specifying the calendar used

        ! end of data_runcontrol
        !-----------------------------------------------------------------------

        USE data_fields, ONLY:      &
            rlat,                   & ! geographical latitude                   ( rad )
            sun_el                    ! sun elevation angle                     ( deg )

        ! end of data_fields
        !-----------------------------------------------------------------------

        IMPLICIT NONE

        INTEGER (KIND=iintegers), INTENT(IN) :: &
            ie, je,             & ! dimensions of the fieldscd ..
            istarts, iends,     & ! start and end-indices of the computation
            jstarts, jends,     & ! start and end-indices of the computation
            ntstep                ! actual time step

        REAL (KIND=ireals), INTENT(IN) ::      &
            dt                    ! long time-step

        REAL (KIND=ireals), INTENT(INOUT) ::  &
            day_length(ie,je),  & ! daylength in hours
            f_dyl(ie,je)          ! daylength effect on Vcmax                   ( 0 to 1)


        !=======================================================================
        ! Local parameters:
        ! ----------------------------------------------------------------------
        INTEGER (KIND=iintegers) :: &
            i,                      & ! loop indices
            j,                      & ! loop indices
            nactday                   ! day of the year


        REAL (KIND=ireals)       :: &
            sun_decl,               & ! declanation of the sun
            acthour,                & ! actual hour of the day
            jj,                     & ! actual year
            ztwo,                   & ! year regulation
            ztho,                   & ! angle of year
            !coszen                 & ! cosine zenith angel
            ms_decl,                & ! maximum solar declination               (  rad  )
            temp_dyl, dyl,          & ! temporal and actual daylength
            temp_dyl_max, dyl_max     ! max temporal and actual daylength


        CHARACTER (LEN=14) yactdate1           ! actual date in the form yyyymmddhhmmss
        CHARACTER (LEN=28) yactdate2           ! actual date in the form &
                                               ! wd   dd.mm.yy  hh mm ss UTC

        !- End of header
        !==============================================================================

        !------------------------------------------------------------------------------
        ! Begin subroutine: get_sun_data
        !------------------------------------------------------------------------------

        !---------------------------------------------------------------------------
        ! Section 1: Calculation of daylength and solar declination angle
        !---------------------------------------------------------------------------

        CALL get_utc_date(ntstep, ydate_ini, dt, itype_calendar, &
            yactdate1, yactdate2, nactday, acthour)

        DO j = jstarts, jends
            DO i = istarts, iends
                READ (yactdate1(1:4),'(I4)') jj
                ztwo = 0.681 + 0.2422 * (jj - 1949) - (jj - 1949) / 4
                ztho = 2 * pi * (REAL(nactday,ireals) - 1 + ztwo) / 365.2422

                sun_decl = 0.006918 - 0.399912 * COS(ztho) + 0.070257 * SIN(ztho) - &
                           0.006758 * COS(2.0 * ztho) + 0.000907 * SIN(2.0 * ztho) - &
                           0.002697 * COS(3.0 * ztho) + 0.001480 * SIN(3.0 * ztho)

                day_length(i,j) = 24 / pi * ACOS(-TAN(rlat(i,j)) * TAN(sun_decl))


                !---------------------------------------------------------------
                ! Section 2. Option 2 - Calculation cosine of zenith angle
                !---------------------------------------------------------------
                !coszen = sin(rlat(i,j)) * sin(sun_decl) - &
                !         cos(rlat(i,j)) * cos(sun_decl) * cos(sun_el(i,j) * D_to_R)


                !---------------------------------------------------------------
                ! Section 3: Calculate daylength control for Vcmax
                !---------------------------------------------------------------

                !IF (rlat >= 0.0) THEN
                ms_decl  = 23.4667 * D_to_R
                !ELSE
                !    ms_decl  = (-1.0 * 23.4667) * D_to_R
                !ENDIF

                temp_dyl     = (-1.0 * sin(rlat(i,j)) * sin(sun_decl)) / (cos(rlat(i,j)) * cos(sun_decl))
                temp_dyl_max = (-1.0 * sin(rlat(i,j)) * sin(ms_decl))  / (cos(rlat(i,j)) * cos(ms_decl))

                temp_dyl     = min(1.0, max(-1.0, temp_dyl))
                temp_dyl_max = min(1.0, max(-1.0, temp_dyl_max))

                dyl     = 2.0 * 13750.9871 * acos(temp_dyl)
                dyl_max = 2.0 * 13750.9871 * acos(temp_dyl_max)

                ! calculate dayl_factor as the ratio of (current:max dayl)^2
                f_dyl(i,j) = min(1.0, max(0.01, (dyl * dyl) / (dyl_max * dyl_max)))


            ENDDO
        ENDDO

        RETURN

    END SUBROUTINE get_sun_data




    SUBROUTINE get_stomatal_data(pft, snowdp, ustar_fv, ps, qv_s, zqvlow, lai, sun_angle, &
                                 p_zflsp_par, p_zflsd_par, p_zflsu_par, fwet, fdry, wtl,&
                                 rs_leaf, par_sun, par_sha, ea, l_sun, l_sha, sla_sun, sla_sha)

        USE data_runcontrol, ONLY :   &
            ! 3. controlling the physics
            ! --------------------------
            itype_root,               & ! type of root density distribution
            itype_tran                  ! type of surface to tamospher transfer

        ! end of data_runcontrol
        !------------------------------------------------------------------------------

        IMPLICIT NONE

        INTEGER (KIND=iintegers), INTENT(IN) :: &
            pft                                   ! The type of PFT needs for defining
                                                  ! constatn values from module data_phenology

        REAL (KIND=ireals), INTENT(IN) ::       &
            snowdp,                             & ! The snow depth
            ustar_fv,                           & ! The friction velocity (ustar)                     ( m/s  )
            ps,                                 & ! The surface pressure                              ( pa   )
            qv_s,                               & ! The specific humidity at the surface              (kg/kg )
            zqvlow,                             & ! The specific humidity of lowest atmospheric layer (kg/kg )
            lai,                                & ! The leaf area index
            sun_angle,                          & !
            p_zflsp_par,                        & ! The direct component of PAR at the ground         ( W/m2 )
            p_zflsd_par,                        & ! The diffuse downward component of PAR
                                                  ! at the ground                                     ( W/m2 )
            p_zflsu_par                           ! The diffuse upward component of PAR
                                                  ! at the ground                                     ( W/m2 )



        REAL (KIND=ireals), INTENT(INOUT) ::   &
            fwet,                              & ! The fraction of canopy that is wet (0 to 1)
            fdry,                              & ! The fraction of canopy that is wet (0 to 1)
            wtl,                               & ! The heat conductance for leaf [m/s]
            rs_leaf,                           & ! The leaf boundary layer resistance                 (  s/m )
            par_sun,                           & ! The PAR absorbed per unit lai for sunlit leaves    (w/m**2)
            par_sha,                           & ! The PAR absorbed per unit lai for shaded leaves    (w/m**2)
            ea,                                & ! The vapor pressure of air in the plant canopy      (  pa  )
            l_sun,                             & ! The sunlit leaf area index
            l_sha,                             & ! The shaded leaf area index
            sla_sun,                           & ! The sunlit specific leaf area index                (m^2/gC)
            sla_sha                              ! The shaded specific leaf area index                (m^2/gC)


        !==============================================================================
        ! Local parameters:
        ! -----------------------------------------------------------------------------

        ! Parameters for esai and elai calculations
        REAL (KIND=ireals)             ::   &
            tlai,                           & ! The one-sided leaf area index, no burying by snow
            tsai,                           & ! The one-sided stem area index, no burying by snow
            htop,                           & ! The canopy top (m)
            hbot,                           & ! The canopy bottom (m)
            ol,                             & ! The thickness of canopy layer covered by snow (m)
            fb,                             & ! The fraction of canopy layer covered by snow
            elai,                           & ! The one-sided leaf area index with burying by snow
            esai                              ! The one-sided stem area index with burying by snow


        REAL (KIND=ireals), PARAMETER ::    &
            h2ocan     = 0.0,               & ! Temporal parameter for water content
            leafc      = 25.0,              & ! (kgC/m2) leaf C
            deadstemc  = 5.5,               & ! (kgC/m2) dead stem C
            forc_hgt_u = 30.0                ! The observational height of wind [m] !!!!!!!!!!!!!!!!!! In CLM3.5 - 30 meter

        REAL (KIND=ireals)             ::   &
            taper,                          & ! The ratio of height:radius_breast_height (tree allometry)
            stocking,                       & ! The stems / ha (stocking density)
            dwood                             ! The density of wood (kgC/m^3)



        REAL (KIND=ireals)             ::   &
            cosz,                           & ! The range 0.001 <= sun_angle <= 1.000
            chil,                           & ! The range -0.4 <= pft_CN_par(pft, X_l) <= 0.6
            fau_1,                          & ! The first parametr for calculations
            fau_2,                          & ! The second parameter for calculations
            G_mu,                           & ! The leaf projection in solar direction (0 to 1)
            vai,                            & ! The total leaf area index + stem area index, one sided
            K_light,                        & ! The optical depth direct beam per unit LAI+SAI
            t1,                             & ! The temporary variables
            t2,                             & ! The temporary variables
            f_sun,                          & ! The sunlit fraction of the canopy
            sun_dir,                        & ! The total canopy absorbed indirect from direct       (W/m**2)
            sun_down,                       & ! The sun canopy absorbed indirect from direct         (W/m**2)
            sun_up,                         & ! The sun canopy absorbed indirect from indirect       (W/m**2)
            sha_down,                       & ! The shade canopy absorbed indirect from direct       (W/m**2)
            sha_up,                         & ! The shade canopy absorbed indirect from indirect     (W/m**2)
            sun_atot,                       & ! The sun canopy total absorbed                        (W/m**2)
            sha_atot,                       & ! The shade canopy total absorbed                      (W/m**2)
            laifra,                         & ! The leaf area fraction of canopy
            sun_alf,                        & ! The sun canopy total absorbed by leaves              (W/m**2)
            sha_alf,                        & ! The shade canopy total absored by leaves             (W/m**2)
            sun_aperlai,                    & ! The sun canopy total absorbed per unit LAI           (W/m**2)
            sha_aperlai,                    & ! The shade canopy total absorbed per unit LAI         (W/m**2)
            qaf                               !

        !- End of header
        !==============================================================================

        !------------------------------------------------------------------------------
        ! Begin subroutine: get_initial_data
        !------------------------------------------------------------------------------

        !------------------------------------------------------------------------------
        ! Section 1: Calculation of esai
        !------------------------------------------------------------------------------
        taper      = 200.0
        stocking   = 1000.0
        dwood      = 500.0

        ! convert from stems/ha -> stems/m^2
        stocking = stocking / 10000.0
        ! convert from dwood kg -> g
        dwood = dwood * 1000.0
        ! convert dwood from dry mass -> Carbon
        dwood = dwood * 0.5



        IF (pft_CN_par(pft, SLA_m) > 0.0) THEN
            tlai = (exp(leafc * pft_CN_par(pft, SLA_m) + &
                    log(pft_CN_par(pft, SLA_o))) - pft_CN_par(pft, SLA_o)) / &
                    pft_CN_par(pft, SLA_m)
        ELSE
            tlai = pft_CN_par(pft, SLA_o) * leafc
        ENDIF

        tlai = max(0.0, tlai)


        IF (pft_CN_par(pft, WOODY) == 1.0) THEN
            ! TREE
            tsai = 0.25 * tlai
            htop = ((3.0 * deadstemc * taper * taper)/(pi * stocking * dwood))**(1.0 / 3.0)  !!!
            htop = min(htop,(forc_hgt_u / (pft_CN_par(pft, R_DISP) + pft_CN_par(pft, R_ZOM))) -3.0)
            htop = max(htop, 0.01)
            hbot = max(0.0, min(3.0, htop - 1.0))
        ELSE
            ! GRASS
            tsai = 0.05 * tlai
            htop = max (0.25, tlai * 0.25)
            htop = min(htop, (forc_hgt_u / (pft_CN_par(pft, R_DISP) + pft_CN_par(pft, R_ZOM))) - 3.0)
            htop = max(htop, 0.01)
            hbot = max(0.0, min(0.05, htop - 0.20))
        ENDIF


        ol   = min(max(snowdp - hbot, 0.0), htop - hbot)
        fb   = 1.0 - ol / max(1.e-06, htop - hbot)
        elai = max(tlai * fb, 0.0)
        esai = max(tsai * fb, 0.0)


        !------------------------------------------------------------------------------
        ! Section 1: Calculation of the leaf boundary layer resistance [s/m]
        !------------------------------------------------------------------------------
        !IF(itype_tran == 1) THEN
        !plant_types == 1
        rs_leaf = 1.0 / TTC_CAN * ((ustar_fv / pft_CN_par(pft, D_LEAF))**(-1.0 / 2.0))
        !ELSE
        !    rs_leaf = 0.0
        !ENDIF

        !------------------------------------------------------------------------------
        ! Section 2: Calculation an optical parameters based on work Sellers (1985)
        !            Calculation of sunlit and shaded parameters for v_cmax25 (sun and sha)
        !            Calculation of mean specific area (SLA) for sunlit and shaded leaves
        !            based on Thornton and Zimmermann, 2007.
        !------------------------------------------------------------------------------

        cosz = max(0.001, sun_angle)
        chil = min(max(pft_CN_par(pft, X_l), -0.4), 0.6)
        IF (abs(chil) <= 0.01) THEN
            chil = 0.01
        ENDIF

        fau_1 = 0.5 - 0.633 * chil - 0.330 * chil**2
        fau_2 = 0.877 * (1.0 - 2.0 * fau_1)
        G_mu  = fau_1 + fau_2 * cosz


        vai = lai + esai ! stems = esai
        IF (sun_angle > 0.0 .and. lai > 0.0 .and. G_mu > 0.0) THEN
            K_light = G_mu / cosz
            t1      = min(K_light * lai, 40.0)
            t2      = exp(-1.0 * t1)
            f_sun   = (1.0 - t2) / t1
            IF (lai > 0.01) THEN
                l_sun = lai * f_sun
                l_sha = lai * (1.0 - f_sun)

                ! calculate the average specific leaf area for sunlit and shaded
                ! canopies, when effective LAI > 0
                sla_sun = (t2 * pft_CN_par(pft, SLA_m) * K_light * lai + &
                           t2 * pft_CN_par(pft, SLA_m) + &
                           t2 * pft_CN_par(pft, SLA_o) * K_light - &
                           pft_CN_par(pft, SLA_m) - &
                           pft_CN_par(pft, SLA_o) * K_light) / &
                           (K_light * (t2 - 1.0))

                sla_sha = ((pft_CN_par(pft, SLA_o) + ((pft_CN_par(pft, SLA_m) * lai) / 2.0)) * &
                           lai - sla_sun * l_sun) / l_sha
            ELSE
                f_sun   = 1.0
                l_sun   = lai
                l_sha   = 0.0
                sla_sun = pft_CN_par(pft, SLA_o)
                sla_sha = 0.0
            ENDIF
        ELSE
            f_sun   = 0.0
            l_sun   = 0.0
            l_sha   = lai
            sla_sun = 0.0
            sla_sha = pft_CN_par(pft, SLA_o) + (pft_CN_par(pft, SLA_m) * lai) / 2.0
        ENDIF

        !------------------------------------------------------------------------------
        ! Section 3: Calculation of the absorbed photosynthetically
        !            active radiation for sunlit and shaded leaves
        !------------------------------------------------------------------------------

        IF (sun_angle > 0.0 .and. lai > 0.0) THEN

            ! 1. calculation direct component of PAR
            sun_dir = max(p_zflsp_par, 0.0)

            ! 2. calculate the total indirect flux absorbed by the sunlit
            !    and shaded canopy based on these fractions

            sun_down = p_zflsd_par * f_sun
            sun_up   = p_zflsu_par * f_sun
            sha_down = p_zflsd_par * (1.0 - f_sun)
            sha_up   = p_zflsu_par * (1.0 - f_sun)

            ! 3. calculate the total flux absorbed in the sunlit and shaded
            !    canopy as the sum of these terms

            sun_atot = sun_dir + sun_down + sun_up
            sha_atot = sha_down + sha_up

            ! 4. calculate the total flux absorbed by leaves in the sunlit
            !    and shaded canopies
            laifra  = lai / vai
            sun_alf = sun_atot * laifra
            sha_alf = sha_atot * laifra

            ! 5. calculate the fluxes per unit lai in the sunlit and shaded
            !    canopies
            IF (l_sun > 0.0) THEN
                sun_aperlai = sun_alf / l_sun
            ELSE
                sun_aperlai = 0.0
            ENDIF

            IF (l_sha > 0.0) THEN
                sha_aperlai = sha_alf / l_sha
            ELSE
                sha_aperlai = 0.0
            ENDIF
        ELSE
            sun_dir     = 0.0
            sun_down    = 0.0
            sun_up      = 0.0
            sha_down    = 0.0
            sha_up      = 0.0
            sun_atot    = 0.0
            sha_atot    = 0.0
            sun_alf     = 0.0
            sha_alf     = 0.0
            sun_aperlai = 0.0
            sha_aperlai = 0.0
        ENDIF

        par_sun = sun_aperlai

        par_sha = sha_aperlai

        !-----------------------------------------------------------------------
        ! Section 3: Calculation canopy air vapor pressure (Pa)
        !-----------------------------------------------------------------------
        qaf = (qv_s + zqvlow) / 2
        ea = (ps * qaf) / 0.622



        !-----------------------------------------------------------------------
        ! Section 4:
        !-----------------------------------------------------------------------


        IF (h2ocan > 0.2) THEN
            ! look fracwet.
            fwet = 1.0
            fwet = min(fwet, 1.0)
        ELSE
            fwet = 0.0
        ENDIF

        fdry = (1.0 - fwet) * lai / vai


        wtl = vai / rs_leaf

        RETURN
    !===========================================================================
    END SUBROUTINE get_stomatal_data




    SUBROUTINE stomata(plant_types, pft, ps, zth_low, t_s, ei, ea, sla, apar, &
                       zf_wat, f_dyl, rs_leaf, rs, psn, v_cmax)

        ! Modules used:
        ! ----------------------------------------------------------------------

        IMPLICIT NONE

        INTEGER (KIND=iintegers), INTENT(IN) :: &
            plant_types,  & ! The type of plants. Can be 1 (C3_grass) or 2 (C4_grass)
            pft             ! The type of PFT needs for defining constatn values from module data_phenology

        REAL (KIND=ireals), INTENT(IN) :: &
            ps,           & ! The surface pressure                              (   Pa  )
            zth_low,      & ! The potential temperature of lowest layer         (   K   )
            t_s,          & ! The soil temperature (main level)                 (   K   )  --> In CLM T_leaf insted of T_s in COSMO
            ei,           & ! The saturation vapour pressure at near            (   Pa  ) ! Change E_I on zepsat   (COSMO) vapor pressure inside leaf (sat vapor press at tl) (pa)
            ea,           & ! The vapor pressure of air in the plant canopy     (   Pa  ) ! ea calculate in subrutine get_stomatal data
            sla,          & ! The specific leaf area index  (sunlit or shaded)  ( m^2/gC)
            apar,         & ! The PAR absorbed per unit lai (sunlit or shaded)  ( W/m^2 )
            zf_wat,       & ! The soil water content                            ( 0 to 1)
            f_dyl           ! The daylength effect on V_cmax                    ( 0 to 1)

        REAL (KIND=ireals), INTENT(INOUT) :: &
            rs_leaf,      & ! The leaf boundary layer resistance                (  s/m )
            rs,           & ! The stomatal resistances                          (  s/m )
            psn,          & ! The foliage photosynthesis leaves                 (umolCO2/m**2/s)
            v_cmax          ! Maximum rate of carboxylation                  (  umol co2/m**2/s )


        !=======================================================================
        ! Local parameters:
        ! ----------------------------------------------------------------------


        REAL (KIND=ireals)  ::   &
            zf_water,        & ! TEST
            recal_rs_coef,   & ! special recalculation coefficient
                               !    for convertation [s m**2 / umol] into [s/m]
            f_t_veg,         & ! mimics thermal function                        ( 0 to 1)
            slamax,          & ! spatial leaf area
            lnc,             & ! leaf N concentration per unit projected LAI    (gN leaf/m^2)
            act,             & ! Rubisco activity                               ( umol/mgRubisco/min  ]
            ppf,             & ! Absorb photosynthetic photon flux              ( umol photons/m**2/s ]
            k_c,             & ! Michaelis-Menten constant for CO2              (  Pa  )
            k_o,             & ! Michaelis-Menten constant for O2               (  Pa  )
            awc,             & ! Intermediate calcuation for wc
            cp,              & ! CO2 compensation point                         (  Pa  )
            !v_cmax,          & ! Maximum rate of carboxylation                  (  umol co2/m**2/s )
            wc,              & ! Rubisco limited photosynthesis                 (  umol co2/m**2/s )
            wj,              & ! Light limited photosynthesis                   (  umol co2/m**2/s )
            we,              & ! Export limited photosynthesis                  (  umol co2/m**2/s )
            cs,              & ! CO2 concentration at leaf surface              (  Pa  )
            a_tmp,           & ! Intermediate calculations for rs
            b_tmp,           & ! Intermediate calculations for rs
            c_tmp,           & ! Intermediate calculations for rs
            q,               & ! Intermediate calculations for rs
            r_s1, r_s2,      & ! Roots for rs                                   (  s/m )
            ci,              & ! Intracellular leaf CO2                         (  Pa  )
            cea,             & ! Constrain ea or else model blows up
            tc                 ! groung surface temperature                     (  C   )

        INTEGER (KIND=iintegers) :: &
            iter               ! the iteration index

        INTEGER (KIND=iintegers), PARAMETER :: &
            niter = 3          ! number of iterations

        REAL (KIND=ireals), PARAMETER :: &
            mpe = 1.e-6        ! prevents overflow error if division by zero

        !-----------------------------------------------------------------------
        ! Section 1. Calculation of coefficients for recalculation of [s/m]
        !            to [s m**2 / umol] and [K] to [C]
        !-----------------------------------------------------------------------
        recal_rs_coef = ps / (rgas * 0.001 * zth_low) * 1.e06
        tc = t_s - t0_melt




        !-----------------------------------------------------------------------
        !Section 2: Calculation of a function that mimics thermal breakdown
        !           of metabolic process
        !-----------------------------------------------------------------------
        f_t_veg = 1.0 + exp((-2.2e05 + 710.0 * (tc + t0_melt)) / &
                               (rgas * 0.001 * (tc + t0_melt)))

        !-----------------------------------------------------------------------
        ! Section 3. Calculation of area based leaf nitrogen concentration
        !            for sunlit and shaded leaves [g N m^-2 leaf area] based on
        !            Thornton and Zimmermann, 2007 approach
        !-----------------------------------------------------------------------

        slamax = max(1.e-5, sla)
        lnc = 1.0 / (pft_CN_par(pft, CN_L) * slamax)
        act = ALPHA_R_25 * ALPHA_VMAX**((tc - 25.0) / 10.0)
        v_cmax = lnc * pft_CN_par(pft, F_LNR) * F_NR * act / f_t_veg * &
                                        zf_wat * pft_CN_par(pft, F_N) * f_dyl

        IF (zf_wat == 0) THEN
            zf_water = 0.2
        ELSE
            zf_water = zf_wat
        ENDIF

        IF (apar <= 0.0) THEN ! night time
            rs  = min(RSMAX0, 1.0 / GLMIN * recal_rs_coef)
            psn = 0.0

        ELSE
            ! Calculation of the absorb photosynthetic photon flux
            ppf = 4.6 * apar
            ! Calculation of the Michaelis-Menten constants [Pa]
            !                                    and CO2 compensation point [Pa]
            k_c = K_C25 * ALPHA_KC**(( tc - 25.0) / 10.0)
            k_o = K_O25 * ALPHA_KO**(( tc - 25.0) / 10.0)
            awc = k_c * (1.0 + CON_O2/k_o)
            cp = 0.5 * k_c/k_o * 0.21 * CON_O2

            ! Calculation of the intracellular leaf CO2 (Pa) and the constrain
            !                                          ea or else model blows up
            IF (plant_types == 1) THEN
                ci = 0.7 * CON_CO2
                cea = max(min(ea, ei), 0.25 * ei)
            ELSE
                ci = 0.4 * CON_CO2
                cea = max(min(ea, ei), 0.4 * ei)
            ENDIF

            ! Convertation [s/m] in [s m**2 / umol]
            rs_leaf = rs_leaf / recal_rs_coef

            ! Calculation of stomatal resistance and leaf photosynthesis
            DO iter = 1, niter
                IF (plant_types == 1) THEN
                    !-----------------------------------------------------------
                    ! Calculation of photosynthesis in C3 plants is based on
                    !                        the model of Farquhar et. al. 1980
                    !-----------------------------------------------------------
                    wc = max(ci - cp, 0.0) * v_cmax / (ci + awc)
                    wj = max(ci - cp, 0.0) * (pft_CN_par(pft, ALPHA) * ppf) / (ci + 2.0 * cp)
                    we = 0.5 * v_cmax
                ELSE
                    !-----------------------------------------------------------
                    ! Calculation of photosynthesis in C4 plants is based on
                    !                         the model of Collatz et. al. 1992
                    !-----------------------------------------------------------
                    wc = v_cmax
                    wj = pft_CN_par(pft, ALPHA) * ppf
                    we = 4000.0 * v_cmax * ci / ps
                ENDIF

                psn = min(wc, wj, we)
                cs  = max(CON_CO2 - 1.37 * rs_leaf * ps * psn, mpe)

                !---------------------------------------------------------------
                !Calculation of stomatal resistance is based on
                !                                the Ball-Berry (1988) approach
                !---------------------------------------------------------------
                a_tmp =  pft_CN_par(pft, MP) * psn * ps * cea  / (cs * ei) + GLMIN
                b_tmp = (pft_CN_par(pft, MP) * psn * ps  / cs + GLMIN) * rs_leaf - 1.0
                c_tmp = - rs_leaf

                IF (b_tmp >= 0.0) THEN
                    q = -0.5 * (b_tmp + sqrt(b_tmp * b_tmp - 4.0 * a_tmp * c_tmp))
                ELSE
                    q = -0.5 * (b_tmp - sqrt(b_tmp * b_tmp - 4.0 * a_tmp * c_tmp))
                ENDIF
                r_s1 = q / a_tmp
                r_s2 = c_tmp / q
                rs = max(r_s1, r_s2)
                ci = max(cs - psn * ps * 1.65 * rs, 0.0)
            ENDDO

            rs = min(RSMAX0, rs * recal_rs_coef)
            rs_leaf = rs_leaf * recal_rs_coef
        ENDIF
        RETURN
    END SUBROUTINE stomata

END MODULE src_phenology



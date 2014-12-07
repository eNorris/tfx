!- Independent case
!*fn r=*\n p=*\n      !- Save new restart and punch files
!*fn tf=* tg=* fa=*   !- Save track and angular flux files
*fn b=phantom.parts  !- Describes the phantom model geometry
!

DIM
  'MXBDY', 1000/

TTL Model of CT Scan about a patient phantom
!
!- Save Restart Case
RES New CASE01 Null 0

!- Integration Parameters (Solve Forward and Backward Directions including Z-axis)
! IGEOG=2  2-D solver
! IDIRG=0  Both forward and backward scattering
! DYGAM=y  Distance in radial plane
! DZGAM=z  Distance in axial direction
! NVGAM=n  Number of angles (should use an even number)
! IQAXG=1  Allows ray tracing in cardinal directions
! EPSGAM=e Convergance criterion
! 
!TRP:G IGEOG=2 IDIRG=0 DYGAM=0.025 DZGAM=0.025  NPOLG=10 IQAXG=1 EPSGAM=0.010
!TRP:G IGEOG=3 IDIRG=0  DYGAM=0.5   DZGAM=0.5    NPOLG=5 IQAXG=1 EPSGAM=0.3
TRP:G IGEOG=3 IDIRG=0  DYGAM=0.5   DZGAM=0.5    NPOLG=5 IQAXG=0 EPSGAM=0.3

!- Gamma Source
SRC
  0, 54.0, 0.0, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 49.8894947556, 20.6649053477, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 38.1837661841, 38.1837661841, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 20.6649053477, 49.8894947556, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 3.3065463577e-15, 54.0, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -20.6649053477, 49.8894947556, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -38.1837661841, 38.1837661841, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -49.8894947556, 20.6649053477, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -54.0, 0.0, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -49.8894947556, -20.6649053477, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -38.1837661841, -38.1837661841, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, -20.6649053477, -49.8894947556, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 9.91963907309e-15, -54.0, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 20.6649053477, -49.8894947556, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 38.1837661841, -38.1837661841, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
  0, 49.8894947556, -20.6649053477, 0.5 /
  52*0., 33*0., 2.80E+13, 1.28E+13, 4.61E+13, 1.32E+14, 5.45E+13, 1.24E+14, 6.83E+13, 1.97E+12, 0.0/
/

!- Material Data (in Number Densities)
MAT:AIR         0.  801603=4.60E-5/
MAT:COLLIMATOR  0. 8200003=3.30E-2/
MAT:PMMA        1.19 100111=8.0  801611=32.0  601203=60.0/
MAT:ALUM        2.70 1302703=100./

!- Parts & Solution Geometry Descriptions
GEO:0
'PHANTOM' 'phantom_part'/
  /
  'PMMA:1'/
'SLICE1' 'slice_part1'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE2' 'slice_part2'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE3' 'slice_part3'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE4' 'slice_part4'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE5' 'slice_part5'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE6' 'slice_part6'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE7' 'slice_part7'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE8' 'slice_part8'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE9' 'slice_part9'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE10' 'slice_part10'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE11' 'slice_part11'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE12' 'slice_part12'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE13' 'slice_part13'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE14' 'slice_part14'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE15' 'slice_part15'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'SLICE16' 'slice_part16'/
  /
  'COLLIMATOR:1', 'AIR:1', 'ALUM:1'/
'BOUNDS' 'extern_part'/
  /
  'AIR:1'/
/ END of GEO:

!- Describe Air & Collimator Regions
LAT
+PHANTOM:1/
  0, 0, 0.0, 0/
+SLICE1:1/
  0, 0, 0, 0/
+SLICE2:1/
  0, 0, 0, 0/
+SLICE3:1/
  0, 0, 0, 0/
+SLICE4:1/
  0, 0, 0, 0/
+SLICE5:1/
  0, 0, 0, 0/
+SLICE6:1/
  0, 0, 0, 0/
+SLICE7:1/
  0, 0, 0, 0/
+SLICE8:1/
  0, 0, 0, 0/
+SLICE9:1/
  0, 0, 0, 0/
+SLICE10:1/
  0, 0, 0, 0/
+SLICE11:1/
  0, 0, 0, 0/
+SLICE12:1/
  0, 0, 0, 0/
+SLICE13:1/
  0, 0, 0, 0/
+SLICE14:1/
  0, 0, 0, 0/
+SLICE15:1/
  0, 0, 0, 0/
+SLICE16:1/
  0, 0, 0, 0/
+BOUNDS:1/
  0, 0, 0, 0/
/
!- Input volumes
*rd GAT.inp
!
!- Specify Boundary Conditions
! v00 denotes all Vacuum boundaries and no symmetry
BND:v00 -80, 80, -80, 80, 0, 1 / RPP
!BND:v00 -80, 80, -80, 80, 0.000001, .999999 / 1 / RPP

!- Print & Punch Options
PRI
  1/
  10, 1/ Edit Body Info
  70, 1/ Edit N & G Fluxes
/
PUN:50, 1,1
PUN:80, 0,1,1
!
!- Translate to MCNP
!TRA
!  3 0/
!- Start Flux Calculation
STA

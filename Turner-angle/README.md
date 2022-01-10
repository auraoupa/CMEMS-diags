# Density compensation between horizontal temperature and salinity gradients

__author__ : Aurélie Albert, Julien Le Sommer (MEOM, IGE)

__context__ : 22-GLO-HR project : Lot 1 - Ocean Modelling

__date__ : 23 September 2019

__purpose__ : Ratio of horizontal surface gradients of temperature and salinity 

__detailed description__ : 

We illustrate the ratio of horizontal surface gradients of temperature and salinity by 
  - 1- plotting the angle between the gradients and the turner angle (arctan(R)) on a polar plot
  - 2- showing histograms of the complex Turner angle
  - 3- showing histograms of surface horizontal gradients of buoyancy and spicyness

__practical steps__ :

Preliminary steps :

for diag 1 :
1. compute horizontal gradients of surface temperature and salinity and thermal and haline expansion terms from surface outputs of NATL60-CJM165 simulation directly on occigen where the outputs are stored, we store the angle the ratio of gradients and the Turner angle : [compute-phase-turner-angle-complex-ratio.ipynb](compute-phase-turner-angle-complex-ratio.ipynb)
1. plot on a polar projection the angle and the turner angle : [polar-plot-phi-turner-angle.ipynb](polar-plot-phi-turner-angle.ipynb)

for diag 2 :
1. compute horizontal gradients of surface temperature and salinity and thermal and haline expansion terms from surface outputs of NATL60-CJM165 simulation directly on occigen where the outputs are stored, we store the complex Turner angle : [compute-turner-angle-complex.ipynb](compute-turner-angle-complex.ipynb)
1. plot histograms of complex Turner angle : [hist-turner-angle-complex.ipynb](hist-turner-angle-complex.ipynb)

for diag 3 :
1. compute horizontal gradients of surface buoyancy and spicyness from surface outputs of NATL60-CJM165 simulation directly on occigen where the outputs are stored, we store the complex Turner angle : [compute-grad-buoyancy-spice.ipynb](compute-grad-buoyancy-spice.ipynb)
1. plot histograms of gradients of buoyancy and spicyness : [hist-grad-buoy-spice.ipynb](hist-grad-buoy-spice.ipynb)


__external libraries needed to run this script__ : 

 * seaborn : only for histogram colors
 
__licence__ : This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

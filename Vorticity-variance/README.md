# README

Vorticity of surface flows in a key indicator of fine scale turbulent flows. Recent observational and modelling studies have shown that submesoscale vorticity fields exhibit a strong seasonal cycle with more fine scale structures in late winter. This is in particular visible in snapshots of surface vorticity. The purpose of the proposed metrics is to provide a quantive measure of this fine scale variance. The metrics provides a pointwise measure of fine scale variance in boxes of about 1° x 1° and over 1 month. This allows to estimate how numerical choices affect the ability of model configurations to reproduce the space and time variability of fine scale vorticity variance. 


## Python librairies used 

You can download them via conda (https://www.continuum.io/downloads) or pip or your favorite packages manager...

  - numpy
  - xarray
  - matplotlib
  - time, sys
  - netCDF4

## Lanczos2DHighPass.py script

This script filters a 2D field of data with Lanczos windowing method and writes the filtered signal in a new file that has the same structure than the input file.

It is possible to filter one or multiple files (same variable) and maps of total and filtered signal can also be produced.

External module needed :
  - WavenumberSpectrum : https://github.com/lesommer/codes/blob/master/WavenumberSpectrum.py
  - oocgcm filtering module : https://github.com/lesommer/oocgcm

Examples of use :

  - filter multiple files and no plot :

```
python Lanczos2DHighPassFilter.py -v 'socurloverf' /media/extra/DATA/NATL60/NATL60-CJM165-S/NATL60-CJM165_y2013m03d1*.1d_curloverf.nc 80 0.0125

```

  - filter one file and plot :

```
python Lanczos2DHighPassFilter.py -v 'socurloverf' -s  /media/extra/DATA/NATL60/NATL60-CJM165-S/NATL60-CJM165_y2013m03d09.1d_curloverf.nc -s -p /media/extra/DATA/NATL60/NATL60-CJM165-PLOTS/NATL60-CJM165_y2013m03d09_socurloverf_total_large_small_scales.png 80 0.0125

```

  
## cmems-glo-hr_demo-fine-scale-metrics_01_vorticity-variance_v1.0.ipynb

This notebook is a demonstration of the implementation of the fine scale variance metric applied to surface relative vorticity of NATL60 outputs of March and September 2013.

External module needed :
  - GriddedData : https://github.com/lesommer/codes/blob/master/GriddedData.py
  - WavenumberSpectrum : https://github.com/lesommer/codes/blob/master/WavenumberSpectrum.py
  - oocgcm filtering module : https://github.com/lesommer/oocgcm


Modifications to make before using this notebook :

  - change the repository in which you have put external python modules (in the demo /home/albert/lib/python)
  - change the repository in which you have put data, both total signal and filtered signal (in the demo /media/extra/DATA/NATL60/NATL60-CJM165-S/), and the gridfile (in the demo /media/extra/DATA/NATL60/NATL60-I/)

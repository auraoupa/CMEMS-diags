#!/bin/bash

python 2DLanczosHighPassFilter.py -v 'socurloverf' /media/extra/DATA/NATL60/NATL60-CJM165-S/NATL60-CJM165_y2013m02d*.1d_curloverf.nc 80 0.0125

python 2DLanczosHighPassFilter.py -v 'socurloverf' -p /media/extra/DATA/NATL60/NATL60-CJM165-PLOTS/NATL60-CJM165_y2013m03d01_socurloverf_ssvariance.png /media/extra/DATA/NATL60/NATL60-CJM165-S/NATL60-CJM165_y2013m03d01.1d_curloverf.nc 80 0.0125

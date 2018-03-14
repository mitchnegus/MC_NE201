# HFNG Flux Spectrum Analysis - Jonathan Morrell

This repository contains code to calculate the flux distribution in each of the 5 sample positions in the HFNG sample holder using a Monte Carlo method.  Plots are saved in the `plots` directory, and the mean/stdv energy are printed to the console.

Code has been tested with `python 2.7` on Ubuntu 17.1.  Numpy and Matplotlib are required.

Changing `saveplots` to `False` in the __main__ section will show the plots in matplotlib's interactive plotter.
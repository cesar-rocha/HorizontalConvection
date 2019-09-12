# HorizontalConvection
Materials for JFM paper "The heat flux of horizontal convection: definition of the Nusselt number," in preparation.

[Cesar B Rocha](cbrocha.com) ([WHOI](whoi.edu))
Thomas Bossy ([ENS de Lyon](http://www.ens-lyon.fr)), 
[Navid Constantinou](http://www.navidconstantinou.com) ([ANU](https://www.anu.edu.au)),
[Stefan Llewellyn-Smith](https://sites.google.com/a/eng.ucsd.edu/sgls/)
([MAE/UCSD](http://maeweb.ucsd.edu), [SIO](scripps.ucsd.edu)), 
[William R. Young](http://pordlabs.ucsd.edu/wryoung/) ([SIO](scripps.ucsd.edu)).

## Dedalus
Direct Numerical Simulations of Horizontal Convection are performed with
[Dedalus](http://dedalus-project.org), a spectral framework in python. Dedalus
can be
[installed](https://dedalus-project.readthedocs.io/en/latest/installation.html#installing-the-dedalus-package)
with pip or conda. We ran suite 77 simulations across different three different systems: a MacPro laptop (8 cores), a Linux workstation (24 cores), and a supercomputer at the Australian National University (up to 1000 cores).

## Analysis
The analysis of the results are performed in python3. The basic requirements
are:
 
- h5py >= 2.6.0
- matplotlib
- numpy
- scipy >= 0.13.0



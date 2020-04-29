# Horizontal Convection
Materials for JFM paper "The Nusselt numbers of horizontal convection".

[Cesar B Rocha](http://www.cbrocha.com) ([WHOI](http://whoi.edu)), [Navid
Constantinou](http://www.navidconstantinou.com)
([ANU](https://www.anu.edu.au)), [Stefan Llewellyn-Smith](https://sites.google.com/a/eng.ucsd.edu/sgls/)
([MAE/UCSD](http://maeweb.ucsd.edu), [SIO](scripps.ucsd.edu)), [William R. Young](http://pordlabs.ucsd.edu/wryoung/) ([SIO](scripps.ucsd.edu)).

## Dedalus
Direct Numerical Simulations of Horizontal Convection are performed with
[Dedalus](http://dedalus-project.org), a spectral framework in python. Dedalus
can be
[installed](https://dedalus-project.readthedocs.io/en/latest/installation.html#installing-the-dedalus-package)
with pip or conda. We ran suite 77 simulations plus 20+ test simulations across
four different systems: 

- MacPro laptop (8 cores) 
- System76 laptop (16 cores)
- Linux workstation (24 cores)
- ANU supercomputer (up to 1000 cores)

## Analysis
The analysis of the results are performed in python. The basic requirements
are:
 
- `h5py >= 2.6.0`
- `matplotlib`
- `numpy`
- `scipy >= 0.13.0`

## Getting help
If you run into any trouble when working with Dedalus or our analysis scripts, please
contact us:

- Cesar Rocha ([@cesar-rocha](https://github.com/cesar-rocha), [crocha@whoi.edu](mailto:crocha@whoi.edu))

- Navid Constantinou
  ([@navidcy](https://github.com/navidcy), [navid.constantinou@anu.edu.au](mailto:navid.constantinou@anu.edu.au))




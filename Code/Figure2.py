"""
    Script for 'The heat flux of horizontal convection: 
    definition of the Nusselt number and scaling second paper,' 
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith 
    & W.R. Young, submitted to JFM.

    Figure2.py: snapshot of streamfunction and buoyancy.

    Cesar Rocha et al.
    WHOI, Spring 2019
    
"""

from dedalus import public as de
from dedalus.extras import flow_tools

import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

import logging
logger = logging.getLogger(__name__)

plt.rcParams['contour.negative_linestyle'] = 'solid'
plt.close('all')

# Load snapshots
snaps2D = h5py.File("Data/snapshot-3D-noslip-Ra3p2e11.h5")
                          
wsnap2D = snaps2D['w'][:].mean(axis=1)
usnap2D = snaps2D['u'][:].mean(axis=1)
b2D = snaps2D['b'][:].mean(axis=1)

# Build a dedalus boundary-value problem to calculate
# the streamfunction given the y-averaged velocity (u,w).

# Bases and domain
x_basis = de.Fourier('x', 512, interval=(0, 4), dealias=3/2)
z_basis = de.Chebyshev('z', 128, interval=(0, 1), dealias=3/2)
domain = de.Domain([x_basis, z_basis], grid_dtype=np.float64)

# The BVP problem  
problem = de.LBVP(domain, variables=['psi','psiz'])

# Input (u,w) as parameters
u = domain.new_field()
uz = domain.new_field()
wx = domain.new_field()
u['g'] = usnap2D
w = domain.new_field()
w['g'] = wsnap2D
u.differentiate(1,out=uz)
w.differentiate(0,out=wx)

problem.parameters['uz'] = uz
problem.parameters['u'] = u
problem.parameters['w'] = w
problem.parameters['wx'] = wx

# Elliptic equations
problem.add_equation("dz(psiz) + dx(dx(psi))  = - uz + wx")
problem.add_equation("psiz - dz(psi) = 0")
problem.add_bc("right(psi) = 0")
problem.add_bc("left(psi) = 0")

# Solve the problem
solver = problem.build_solver()
logger.info('Solver built')
solver.solve()

# Get solutions
psi2D = solver.state['psi']['g']
z = snaps2D['z'][:]
x = snaps2D['x'][:]

psi2D -= psi2D.mean()
psi2D = psi2D/psi2D.max()

# Plotting

fig = plt.figure(figsize=(10.5,4.85))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2.5])
cp = np.linspace(-1,1,30)

ax1 = plt.subplot(gs[0])
plt.contour(x,z[25:],psi2D[:,25:].T,cp,vmin=cp.min(),vmax=cp.max())

plt.ylim(0.95,1.)
plt.xlim(0,4)
plt.text(0,1.0025,"(a)")

ax1.set_xticks([])

plt.text(2.75,1.0025,"Streamfunction")

ax2 = plt.subplot(gs[2])
plt.contour(x,z,psi2D.T,cp,vmin=cp.min(),vmax=cp.max())
plt.xlabel(r'$x/h$')
plt.ylabel(r'         $\,\,\,\,\,z/h$')
plt.xlim(0,4)
plt.ylim(0,0.95)

plt.xticks([0,1,2,3,4])
plt.yticks([0,0.2,.4,.6,.8],['0.00','0.20','0.40','0.60','0.80'])

plt.subplots_adjust(wspace=.275, hspace=.04)

ax3 = plt.subplot(gs[1])

cb = np.linspace(-1.,1,25)
plt.contourf(x,z[25:],b2D[:,25:].T,cb,cmap='RdBu_r',vmin=cb.min(),vmax=cb.max())
plt.contour(x,z[25:],b2D[:,25:].T,[-2.,-.75],colors='0.2',linewidths=0.65)
plt.ylim(0.95,1.)
plt.text(0,1.0025,"(b)")

ax3.set_xticks([])
plt.xlim(0,4)
plt.ylim(.95,1)
plt.text(3.2,1.0025,"Buoyancy")

ax4 = plt.subplot(gs[3])

cb = np.linspace(-1.,1,60)
im_b=plt.contourf(x,z,b2D.T,cb,cmap='RdBu_r',vmin=cb.min(),vmax=cb.max())

plt.contour(x,z,b2D.T,[-2.,-.79],colors='0.2',linewidths=0.65)

plt.xlabel(r'$x/h$')
plt.ylabel(r'        $\,\,\,\,\,z/h$')
plt.xlim(0,4)
plt.ylim(0,.9)
plt.xticks([0,1,2,3,4])
plt.yticks([0,0.2,.4,.6,.8],['0.00','0.20','0.40','0.60','0.80'])
cbar_ax = fig.add_axes([.93, .225, 0.02, 0.5])
fig.colorbar(im_b, cax=cbar_ax,ticks=[-1,-0.5,0,.5,1.],label=r'$b/b_*$')

plt.savefig("Figz/Figure2.png",dpi=800, bbox_inches = 'tight',pad_inches = 0)
plt.savefig("Figz/Figure2.eps", bbox_inches = 'tight',pad_inches = 0)

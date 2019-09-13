"""
    Script for 'The heat flux of horizontal convection:
    definition of the Nusselt number and scaling second paper,'
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith
    & W.R. Young, submitted to JFM.

    This is a Dedalus script for no-slip 3D horizontal convection calculations.
    It uses a Fourier basis in the x direction with periodic boundary
    conditions and Chebyshev basis in the z direction.

    The equations are scaled in units of Archimedean time scale
    Tb = (h/bmax)^1/2, where bmax is the maximum value of surface buoyancy.
    Note that the paper used Lx--the horizontal domain--instead of h for its
    length scale, thus the numerical Rayleigh number in this script is
    4^3=64 times smaller than in the paper.

    To run using 24 threads, use:
    $ mpiexec -n 24 python3 3D_HC.py

    Snapshots must be merged prior to analysis:
    $ python3 merge.py snapshots/

    Cesar Rocha et al.
    WHOI, Summer 2018
"""

import numpy as np
from mpi4py import MPI
import time

from dedalus import public as de
from dedalus.extras import flow_tools

import logging
logger = logging.getLogger(__name__)

# Parameters
Lx, Ly, Lz = (4., 1., 1.)
Ra = 1.*1e7
Pr = 1
k = np.pi/(Lx)

# Create bases and domain
x_basis = de.Fourier('x', 256, interval=(0, Lx), dealias=3/2)
y_basis = de.Fourier('y', 64, interval=(0, Ly), dealias=3/2)
z_basis = de.Chebyshev('z', 64, interval=(0, Lz), dealias=3/2)
domain = de.Domain([x_basis, y_basis, z_basis], grid_dtype=np.float64)

# Nondimensional 3D Boussinesq hydrodynamics
problem = de.IVP(domain, variables=['p','b','u','v','w','bz','uz','wz','vz','bx','by'])
problem.meta['p','b','u','w','v']['z']['dirichlet'] = True
problem.parameters['P'] = (Ra * Pr)**(-1/2)
problem.parameters['R'] = (Ra / Pr)**(-1/2)
problem.parameters['k'] = k
problem.add_equation("dx(u) + dy(v) + wz = 0")
problem.add_equation("dt(b) - P*(dx(dx(b)) + dy(dy(b)) + dz(bz))             = -(u*dx(b) + v*dy(b) + w*bz)")
problem.add_equation("dt(u) - R*(dx(dx(u)) + dy(dy(u)) + dz(uz)) + dx(p)     = -(u*dx(u) + v*dy(u) + w*uz)")
problem.add_equation("dt(v) - R*(dx(dx(v)) + dy(dy(v)) + dz(vz)) + dy(p)     = -(u*dx(v) + v*dy(v) + w*vz)")
problem.add_equation("dt(w) - R*(dx(dx(w)) + dy(dy(w)) + dz(wz)) + dz(p) - b = -(u*dx(w) + v*dy(w) + w*wz)")
problem.add_equation("bx - dx(b) = 0")
problem.add_equation("by - dy(b) = 0")
problem.add_equation("bz - dz(b) = 0")
problem.add_equation("uz - dz(u) = 0")
problem.add_equation("wz - dz(w) = 0")
problem.add_equation("vz - dz(v) = 0")
problem.add_bc("left(bz) = 0")
problem.add_bc("left(u) = 0")  # For free-slip, change this to left(uz)=0.
problem.add_bc("left(v) = 0")  # For free-slip, change this to left(vz)=0.
problem.add_bc("left(w) = 0")
problem.add_bc("right(b) = cos(2*k*x)")
problem.add_bc("right(u) = 0") # For free-slip, change this to right(uz)=0.
problem.add_bc("right(v) = 0") # For free-slip, change this to right(vz)=0.
problem.add_bc("right(w) = 0", condition="(nx !=0)")
problem.add_bc("right(p) = 0", condition="(nx == 0)")

# Build solver
solver = problem.build_solver(de.timesteppers.RK443)
logger.info('Solver built')

# Initial conditions (motionless and homogeneous with b=0)
x = domain.grid(0)
z = domain.grid(1)
b = solver.state['b']
bz = solver.state['bz']
b['g'] = 0.
b.differentiate('z', out=bz)

# Initial timestep
dt = 0.125

# Integration parameters
solver.stop_sim_time = 2500
solver.stop_wall_time = np.inf
solver.stop_iteration = np.inf

# Analysis
snapshots = solver.evaluator.add_file_handler('snapshots', sim_dt=25, max_writes=20)
snapshots.add_task("b", name="b")
snapshots.add_task("u", name="u")
snapshots.add_task("v", name="v")
snapshots.add_task("w", name="w")
#snapshots.add_system(solver.state) # Save everything

# y-averaged sections
analysis1 = solver.evaluator.add_file_handler("2d_averages", sim_dt=0.25,max_writes=50)
analysis1.add_task("integ(b,'y')", name="b")
analysis1.add_task("integ(bz,'y')", name="bz")
analysis1.add_task("integ(u,'y')", name="u")
analysis1.add_task("integ(w,'y')", name="w")

# Diagnostics
analysis2 = solver.evaluator.add_file_handler("diagnostics", iter=10)
analysis2.add_task("integ(0.5 * (u*u + v*v +  w*w))/4", name="ke")
analysis2.add_task("integ(0.5 * (u*u))/4", name="u2")
analysis2.add_task("integ(0.5 * (v*v))/4", name="v2")
analysis2.add_task("integ(0.5 * (w*w))/4", name="w2")
analysis2.add_task("integ( P*(bx*bx + by*by + bz*bz))/4", name="chi")
analysis2.add_task("integ( P*(bx*bx))/4", name="bx2")
analysis2.add_task("integ( P*(by*by))/4", name="by2")
analysis2.add_task("integ( P*(bz*bz))/4", name="bz2")
analysis2.add_task("integ(w*b)/4", name="wb")

# CFL
CFL = flow_tools.CFL(solver, initial_dt=dt, cadence=4, safety=1,
                     max_change=1.5, min_change=0.5, max_dt=0.125, threshold=0.05)
CFL.add_velocities(('u', 'v', 'w'))

# Flow properties
flow = flow_tools.GlobalFlowProperty(solver, cadence=10)
flow.add_property("sqrt(u*u + v*v + w*w) / R", name='Re')
flow.add_property("(u*u + v*v + w*w)/2", name='K')

# Main loop
try:
    logger.info('Starting loop')
    start_time = time.time()
    while solver.ok:
        dt = CFL.compute_dt()
        dt = solver.step(dt)
        if (solver.iteration-1) % 10 == 0:
            logger.info('Iteration: %i, Time: %e, dt: %e' %(solver.iteration, solver.sim_time, dt))
except:
    logger.error('Exception raised, triggering end of main loop.')
    raise
finally:
    end_time = time.time()
    logger.info('Iterations: %i' %solver.iteration)
    logger.info('Sim end time: %f' %solver.sim_time)
    logger.info('Run time: %.2f sec' %(end_time-start_time))
    logger.info('Run time: %f cpu-hr' %((end_time-start_time)/60/60*domain.dist.comm_cart.size))

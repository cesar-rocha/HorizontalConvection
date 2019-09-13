"""
    Script for 'The heat flux of horizontal convection:
    definition of the Nusselt number and scaling second paper,'
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith
    & W.R. Young, submitted to JFM.

    This is a Dedalus script for no-slip 2D horizontal convection calculations. 
    It uses a Fourier basis in the x direction with periodic boundary
    conditions and Chebyshev basis in the z direction.

    The equations are scaled in units of Archimedean time scale 
    Tb = (h/bmax)^1/2, where bmax is the maximum value of surface buoyancy.
    Note that the paper used Lx--the horizontal domain--instead of h for its    length scale, thus the numerical Rayleigh number in this script is 
    4^3=64 times smaller than in the paper.

    To run using 24 threads, use:
    $ mpiexec -n 24 python3 2D_HC.py

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
Lx, Lz = (4., 1.)
Ra = 1.*1e9
Pr = 1
k = np.pi/(Lx)

# Create bases and domain
x_basis = de.Fourier('x', 1024, interval=(0, Lx), dealias=3/2)
z_basis = de.Chebyshev('z', 256, interval=(0, Lz), dealias=3/2)
domain = de.Domain([x_basis, z_basis], grid_dtype=np.float64)

# Non-dimensional 2D Boussinesq hydrodynamics
problem = de.IVP(domain, variables=['p','b','u','w','bz','uz','wz','bx'])
problem.meta['p','b','u','w']['z']['dirichlet'] = True
problem.parameters['P'] = (Ra * Pr)**(-1/2)
problem.parameters['R'] = (Ra / Pr)**(-1/2)
problem.parameters['k'] = k
problem.add_equation("dx(u) + wz = 0")
problem.add_equation("dt(b) - P*(dx(dx(b)) + dz(bz))             = -(u*dx(b) + w*bz)")
problem.add_equation("dt(u) - R*(dx(dx(u)) + dz(uz)) + dx(p)     = -(u*dx(u) + w*uz)")
problem.add_equation("dt(w) - R*(dx(dx(w)) + dz(wz)) + dz(p) - b = -(u*dx(w) + w*wz)")
problem.add_equation("bz - dz(b) = 0")
problem.add_equation("bx - dx(b) = 0")
problem.add_equation("uz - dz(u) = 0")
problem.add_equation("wz - dz(w) = 0")
problem.add_bc("left(bz) = 0")
problem.add_bc("left(u) = 0")  # For free-slip, change this to left(uz) = 0.
problem.add_bc("left(w) = 0")
problem.add_bc("right(u) = 0") # For free-slip, change this to right(uz) = 0.
problem.add_bc("right(b) = cos(2*k*x)")
problem.add_bc("right(w) = 0", condition="(nx != 0)")
problem.add_bc("right(p) = 0", condition="(nx == 0)")

# Build solver
solver = problem.build_solver(de.timesteppers.RK443)
logger.info('Solver built')

# Initial conditions
x = domain.grid(0)
z = domain.grid(1)
b = solver.state['b']
bz = solver.state['bz']

# Random perturbations, initialized globally for same results in parallel
gshape = domain.dist.grid_layout.global_shape(scales=1)
slices = domain.dist.grid_layout.slices(scales=1)
rand = np.random.RandomState(seed=42)
noise = rand.standard_normal(gshape)[slices]

# Coldish fluid in the container
b['g'] = -0.6
b.differentiate('z', out=bz)

# Integration parameters
solver.stop_sim_time = 18000
solver.stop_wall_time = np.inf
solver.stop_iteration = np.inf
dt = 0.125 # Initial time step

# Analysis
snapshots = solver.evaluator.add_file_handler("snapshots", sim_dt=2, max_writes=200)
snapshots.add_task("b", name="b")
snapshots.add_task("bz", name="bz")
snapshots.add_task("u", name="u")
snapshots.add_task("w", name="w")
#snapshots.add_system(solver.state)  # Save all fields

# Diagnostics
analysis2 = solver.evaluator.add_file_handler("diagnostics", iter=10)
analysis2.add_task("integ(0.5 * (u*u + w*w))/4", name="ke")
analysis2.add_task("integ( P*(bx*bx + bz*bz))/4", name="chi")
analysis2.add_task("integ( R*(dx(u)*dx(u) + uz*uz + dx(w)*dx(w) + wz*wz) )/4", name="ep")
analysis2.add_task("integ(w*b)/4", name="wb")

# CFL
CFL = flow_tools.CFL(solver, initial_dt=dt, cadence=10, safety=1,
                     max_change=1.5, min_change=0.5, max_dt=0.125, threshold=0.05)
CFL.add_velocities(('u', 'w'))

# Flow properties
flow = flow_tools.GlobalFlowProperty(solver, cadence=10)
flow.add_property("sqrt(u*u + w*w) / R", name='Re')
flow.add_property("(u*u + w*w)/2", name='K')

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

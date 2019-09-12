"""
    Script for 'The heat flux of horizontal convection:
    definition of the Nusselt number and scaling second paper,'
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith
    & W.R. Young, submitted to JFM.

    Figure4.py: time series of kinetic energy, Nusselt number, and
                bottom buoyancy for 2D solutions with Ra=6.4e9.

    Cesar Rocha et al.
    WHOI, Spring 2019

"""


import matplotlib.pyplot as plt
import numpy as np
import h5py

# Load data
Nu_ns = np.load("../Data/NuAndKE_nostress.npz")
Nu_sl = np.load("../Data/NuAndKE_noslip.npz")
Bb_ns = np.load("../Data/BottomBuoyancy_nostress.npz")
Bb_sl = np.load("../Data/BottomBuoyancy_noslip.npz")

# Normalization factor (diffusive time scale)
Tkappa = 1e4

# Plotting
fig = plt.figure(figsize=(8.5,10.5))

ax1 = fig.add_subplot(311)

plt.semilogy(Nu_ns['time']/Tkappa,Nu_ns['ke'],'b')
plt.semilogy(Nu_sl['time']/Tkappa,Nu_sl['ke'],'r')

plt.xlim([-0.005,.6])
plt.ylim([5e-4,.045])

plt.ylabel(r'$\langle u^2 + w^2 \rangle/2 h b_*$')
plt.text(0,0.0455,'(a)')

plt.xlabel(r'$\kappa\, t /h^2$')

ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax2 = fig.add_subplot(312)

plt.plot(Nu_ns['time']/Tkappa,Nu_ns['Nu'],'b')
plt.plot(Nu_sl['time']/Tkappa,Nu_sl['Nu'],'r')

plt.text(.45,26,'free-slip',color='b')
plt.text(.4,11.,'no-slip',color='r')

plt.xlim([-0.005,.6])
plt.ylim([0,55])

plt.xlabel(r'$\kappa\, t /h^2$')

ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.ylabel(r'Nu')
plt.text(0,56,'(b)')

plt.xlabel(r'$\kappa\, t /h^2$')

ax3 = fig.add_subplot(313)

plt.plot(Bb_ns['time']/Tkappa,Bb_ns['b'],'b')
plt.plot(Bb_sl['time']/Tkappa,Bb_sl['b'],'r')

plt.xlim([-0.005,.6])

ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)

plt.ylabel(r'$\bar{b}(0)/b_*$')
plt.xlabel(r'$\kappa\, t /h^2$')
plt.text(0,0.045,'(c)')

plt.yticks([0,-.25,-.5,-.75])

plt.savefig("../Figz/Figure4.png",dpi=400, bbox_inches = 'tight',
    pad_inches = 0)
plt.savefig("../Figz/Figure4.eps", bbox_inches = 'tight',
    pad_inches = 0)


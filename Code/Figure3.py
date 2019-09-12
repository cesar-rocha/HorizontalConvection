"""
    Script for 'The heat flux of horizontal convection:
    definition of the Nusselt number and scaling second paper,'
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith
    & W.R. Young, submitted to JFM.

    Figure3.py: surface buoyancy and lateral buoyancy flux and
                and a "effective diffusive" flux.

    Cesar Rocha et al.
    WHOI, Spring 2019
"""


import matplotlib.pyplot as plt
import numpy as np
import h5py

# Load data
data = np.load("../Data/BuoyancyAndFlux_Ra6p4e10.npz")

# Plotting
fig = plt.figure(figsize=(12,4))

ax = fig.add_subplot(121)
plt.plot(data['x'],data['F'],'b')
plt.xlabel(r"$x/h$")
plt.text(-.1,78,"(a)")

ax2 = ax.twinx()
ax2.plot(data['x'],data['bs'],'k--')
plt.xlabel(r"$x/h$")
ax2.set_ylabel(r"$b_s/b_*$")
plt.text(2.78,0,r"$b_s$")

plt.yticks([-1,-.5,0,.5,1.])

ax.set_ylabel("$h \, F/\kappa b_*$")
plt.title(r'$F(x)$')

plt.subplots_adjust(wspace=.5, hspace=None)

ax = fig.add_subplot(122)
plt.plot(data['x'],data['Jx'],'b')
plt.plot(data['x'],data['Jx_pred'],'k--')
plt.text(1.88,65.6,r'$-D \partial_x b_s$')
plt.xlabel(r"$x/h$")
plt.ylabel(r"$h\, J/ \kappa b_*$")
plt.title(r'$J(x)$')

plt.text(-.1,286,"(b)")

plt.savefig("../Figz/Figure3.png", bbox_inches = 'tight',
    pad_inches = 0)
plt.savefig("../Figz/Figure3.eps", bbox_inches = 'tight',
    pad_inches = 0)



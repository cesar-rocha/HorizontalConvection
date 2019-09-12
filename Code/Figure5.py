"""
    Script for 'The heat flux of horizontal convection:
    definition of the Nusselt number and scaling second paper,'
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith
    & W.R. Young, submitted to JFM.

    Figure4.py: time series of Nusselt number for 2D and 3D
                free-slip and no-slip solutions with Ra=6.4e9,
                with a "cold start."

    Cesar Rocha et al.
    WHOI, Spring 2019

"""

import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# Load data
data2d_nostress = np.load('../Data/NuAndKE_2D_nostress_6p4e10.npz')
data2d_noslip = np.load('NuAndKE_2D_noslip_6p4e10.npz')
data3d_nostress = np.load('NuAndKE_3D_nostress_6p4e10.npz')
data3d_noslip = np.load('NuAndKE_3D_noslip_6p4e10.npz')

# Plotting
fig = plt.figure(figsize=(10,6))
ax = fig.add_subplot(111)

p1 = ax.plot(data3d_nostress['time'],data3d_nostress['Nu'],'b')
ax.plot(data2d_nostress['time'],data2d_nostress['Nu'],'--',color=p1[0].get_color(),linewidth=.5)

ax.plot(data3d_noslip['time'],data3d_noslip['Nu'],'r')
p2 = ax.plot(data2d_noslip['time'],data2d_noslip['Nu'],'r--',linewidth=.5)

plt.xlim(-0.005,0.125)
plt.ylim(0,100)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.text(.07,45.5,'free-slip',color='b')
plt.text(.11,22.5,'no-slip',color='r')

plt.xlabel(r'$\kappa t/h^2 $')
plt.ylabel(r'Nu')

plt.text(.125,44.9,'3D')
plt.text(.125,35.5,'2D')
plt.text(.125,30.75,'3D')
plt.text(.125,26.7,'2D')

plt.savefig("Figure5.png", bbox_inches = 'tight',
            pad_inches = 0)

plt.savefig("Figure5.eps", bbox_inches = 'tight',
            pad_inches = 0)

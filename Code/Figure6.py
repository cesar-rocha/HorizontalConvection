
"""
    Script for 'The heat flux of horizontal convection: 
    definition of the Nusselt number and scaling second paper,' 
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith 
    & W.R. Young, submitted to JFM.

    Figure6.py: log vs. log Ra-Nu diagram.

    Cesar Rocha et al.
    WHOI, Spring 2019
    
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

plt.close('all')

# Load data
data = np.load("../Data/NuVsRa.npz")

# Plotting
fig = plt.figure(figsize=(8.5,6.5))

ax = fig.add_subplot(111)

plt.loglog(data['Ra_2D_FS'],data['Nu_2D_FS'],'b.',markersize=10,
           markerfacecolor='none')
plt.loglog(data['Ra_2D_NS'],data['Nu_2D_NS'],'rs',markersize=4,
           markerfacecolor='none')
plt.loglog(data['Ra_3D_NS'],data['Nu_3D_NS'],'rs',markersize=4)
plt.loglog(data['Ra_3D_FS'],data['Nu_3D_FS'],'bo',markersize=5)

Ras = 8*np.array([4e5,1e11])
plt.loglog(Ras,.13*(Ras**(1/5)),'k',linewidth=1)
Ras = 8*np.array([1e11,1e13])
plt.loglog(Ras,.033*(Ras**(1/4)),'k',linewidth=1)

plt.text(6.4e9,10,r'Ra$^{1/5}$')
plt.text(1.2e13,52,r'Ra$^{1/4}$')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

Ras = np.linspace(1e-1, 5e3, 100)
Ras1 = np.linspace(1e-1, 2e4, 100)
plt.plot(8*Ras, np.ones(np.size(Ras)) + (Ras/2695.9)**2,'k--',linewidth=1)
plt.plot(8*Ras1, np.ones(np.size(Ras1)) + (Ras1/10973.7)**2,'k--',linewidth=1)

plt.plot(.4e10,2.4,'rs')
plt.plot(.7e10,2.4,'bo')
plt.text(1.275e10,2.325,'3D')

plt.plot(.4e10,2.0,'rs',markerfacecolor='none')
plt.plot(.7e10,2.0,'bo',markerfacecolor='none')
plt.text(1.275e10,1.925,'2D')

plt.text(2.5e9,1.45,r'free-slip',color='b')
plt.text(2.5e9,1.15,r'no-slip',color='r')

plt.xlim(1,1e14)
plt.yticks([1,2,5,10,20,40,80,160],["1","2","5","10","20","40","80","160"])

plt.ylabel('Nu')
plt.xlabel(r'Ra')

Ras = np.linspace(1e-1, 1e4, 100)
sub_axes = plt.axes([.2, .525, .25, .25])
sub_axes.plot(data['Ra_2D_FS'],data['Nu_2D_FS'],'b.',markersize=10,
           markerfacecolor='none')
sub_axes.plot(data['Ra_2D_NS'],data['Nu_2D_NS'],'rs',markersize=4,
           markerfacecolor='none')
sub_axes.plot(8*Ras, np.ones(np.size(Ras)) + (Ras/2695.9)**2,'k--',linewidth=1)
sub_axes.plot(8*Ras, np.ones(np.size(Ras)) + (Ras/10973.7)**2,'k--',linewidth=1)
sub_axes.spines['top'].set_visible(False)
sub_axes.spines['right'].set_visible(False)
sub_axes.set_yticks([1,1.1])
sub_axes.set_xlabel(r'Ra$\times 10^{-4}$')
sub_axes.set_ylabel('Nu')
sub_axes.set_xlim(0,4e4)
sub_axes.set_ylim(0.99,1.15)
sub_axes.yaxis.set_label_coords(-0.09,0.45)
sub_axes.xaxis.set_label_coords(0.5,-0.175)

plt.xticks([0,1e4,2e4,3e4,4e4],["0","1","2","3","4"])

plt.savefig("../Figz/Figure6.png",dpi=800)
plt.savefig("../Figz/Figure6.eps")

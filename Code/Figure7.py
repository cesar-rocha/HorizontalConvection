
"""
    Script for 'The heat flux of horizontal convection: 
    definition of the Nusselt number and scaling second paper,' 
    by C.B. Rocha, T. Bossy, N.C. Constantinou, S.G. Llewellyn Smith 
    & W.R. Young, submitted to JFM.

    Figure7.py: log vs. log Ra-Nu diagram.

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
fig = plt.figure(figsize=(8.5,7.5))

ax = fig.add_subplot(211)
p = -1/5

plt.semilogx(data['Ra_2D_FS'],data['Nu_2D_FS']*(data['Ra_2D_FS']**p),'b.',markersize=10,markerfacecolor='none')
plt.semilogx(data['Ra_2D_NS'],data['Nu_2D_NS']*(data['Ra_2D_NS']**p),'rs',markersize=4,markerfacecolor='none')
plt.semilogx(data['Ra_3D_NS'],data['Nu_3D_NS']*(data['Ra_3D_NS']**p),'rs',markersize=4)
plt.semilogx(data['Ra_3D_FS'],data['Nu_3D_FS']*(data['Ra_3D_FS']**p),'bo',markersize=5)

plt.ylabel(r'Nu$\times Ra^{-1/5}$')
plt.xticks([])

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)

plt.xlim(1e3,1e14)
plt.ylim(0.1,.35)

plt.plot([1e3,5e13],[0.168]*2,linewidth=1,color='0.5')
plt.text(4.9e13,0.168,'0.17')
plt.plot([1e3,5e13],[0.213]*2,linewidth=1,color='0.5')
plt.text(4.9e13,0.213,'0.21')
plt.plot([1e3,5e13],[0.243]*2,linewidth=1,color='0.5')
plt.text(4.9e13,0.243,'0.24')

plt.plot(.4e12,.15,'rs')
plt.plot(.7e12,.15,'bo')
plt.text(1.275e12,.095+.05,'3D')
plt.plot(.4e12,.0865+0.04,'rs',markerfacecolor='none')
plt.plot(.7e12,.0865+0.04,'bo',markerfacecolor='none')
plt.text(1.275e12,.0841+0.04,'2D')
plt.text(1601,.3475,'(a)')

ax = fig.add_subplot(212)
p = -1/4

plt.semilogx(data['Ra_2D_FS'],data['Nu_2D_FS']*(data['Ra_2D_FS']**p),'b.',markersize=10,markerfacecolor='none')
plt.semilogx(data['Ra_2D_NS'],data['Nu_2D_NS']*(data['Ra_2D_NS']**p),'rs',markersize=4,markerfacecolor='none')
plt.semilogx(data['Ra_3D_NS'],data['Nu_3D_NS']*(data['Ra_3D_NS']**p),'rs',markersize=4)
plt.semilogx(data['Ra_3D_FS'],data['Nu_3D_FS']*(data['Ra_3D_FS']**p),'bo',markersize=5)

plt.ylabel(r'Nu$\times Ra^{-1/4}$')
plt.xlabel(r'Ra')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

plt.xlim(1e3,1e14)
plt.ylim(0.025,.15)

plt.plot([1e3,5e13],[0.065]*2,linewidth=1,color='0.5')
plt.text(6e13,0.067,'0.065')
plt.plot([1e3,5e13],[0.049]*2,linewidth=1,color='0.5')
plt.text(6e13,0.05,'0.049')

plt.text(1601,.1475,'(b)')

plt.text(3.2e11,.14,r'free-slip',color='b')
plt.text(3.2e11,.1275,r'no-slip',color='r')

plt.savefig("../Data/Figure7.png",dpi=800)
plt.savefig("../Data/Figure7.eps")

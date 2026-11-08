# Composite hedge spot brass with futures on copper and zinc

# import libraries
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd

# import dataset
df=pd.read_excel(r'C:\Users\tarikB\Desktop\Thesis X.xlsx',
                 sheet_name='resolve', skiprows=3,header=None)

ybrass= np.log(df.iloc[:,1]).diff().dropna()
xcopper= np.log(df.iloc[:,2]).diff().dropna()
xzinc= np.log(df.iloc[:,3]).diff().dropna()

# rename
ybrass.name='spot brass'
xcopper.name='f.copper'
xzinc.name='f.zinc'

# define x matrix
x=pd.concat([xcopper,xzinc],axis=1)

# Define X matrix with constant added
X= sm.add_constant(x)

# fitting
model= sm.OLS(ybrass,X).fit()

# extract coefficents from statsmodels
b0= model.params['const']
b1= model.params['f.copper']
b2= model.params['f.zinc']

# Plot regression & diagnostic
fig= plt.figure(figsize=(20,20))

ax1=fig.add_subplot(1,2,1,projection='3d')
ax2=fig.add_subplot(1,2,2)
fig.subplots_adjust(left=0.05, right=0.95, wspace=0.25)

# Set diagnostic
stats= str(model.summary()).split('Notes:')[0]
ax2.axis('off')
ax2.text(-0.1,0.85,stats,fontsize=12,
             fontfamily='monospace',verticalalignment='top')

#Plot regression surface
ax1.scatter(xcopper,xzinc,ybrass,color='darkblue',
            label='Historical data from 2008 to 2026')

ax1.set_title(f'∆Brass(S)={b0:.2f} + {b1:.2f}∆copper(F) + {b2:.2f}∆zinc(F)',
              color='black',fontweight='bold',fontsize=14)

xcopper_surf,xzinc_surf = np.meshgrid(
    np.linspace(min(xcopper),max(xcopper),15),
    np.linspace(min(xzinc),max(xzinc),15))

y_surf= b0+b1*(xcopper_surf)+b2*(xzinc_surf)
ax1.plot_surface(xcopper_surf,xzinc_surf,y_surf,alpha=0.3,
                 cmap='viridis',edgecolor='none',rstride=1,cstride=1)
ax1.set_xlabel('Futures copper log returns',color='black',fontweight='bold',labelpad=10)
ax1.set_ylabel('Futures zinc log returns',color='black',fontweight='bold',labelpad=10)
ax1.set_zlabel('Spot brass log returns',color='black',fontweight='bold',labelpad=10)

ax1.xaxis.pane.fill= False
ax1.yaxis.pane.fill= False
ax1.zaxis.pane.fill= False

ax1.xaxis._axinfo["grid"]['color'] = (0.8, 0.8, 0.8, 0.2)
ax1.yaxis._axinfo["grid"]['color'] = (0.8, 0.8, 0.8, 0.2)
ax1.zaxis._axinfo["grid"]['color'] = (0.8, 0.8, 0.8, 0.2)
ax1.legend(loc='upper left')

plt.show()

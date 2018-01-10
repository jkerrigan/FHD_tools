from scipy.io import readsav
import numpy as np
import pylab as pl



def angulardist(cat_RADEC,cat_flux,deRA,deDEC,deFLUX):
    ### RA/DEC in deg. ###
    return np.argmin(np.sqrt((cat_RADEC[:,0] - deRA)**2 + (cat_RADEC[:,1] - deDEC)**2 +(cat_flux - deFLUX)**2))

catalog = readsav('mwa_calibration_source_list_gleam_kgs_fhd_fornax.sav')
skymodel = readsav('zen.2458042.59528.HH.uvOR_skymodel.sav')

decon_RADEC = np.hstack((skymodel['skymodel'][0][2]['RA'][:,None],skymodel['skymodel'][0][2]['DEC'][:,None]))
decon_I = [I['I'][0] for I in skymodel['skymodel'][0][2]['flux']]

gleam_catRADEC = []
gleam_catI = []

for i in range(np.shape(catalog['catalog'])[0]):
    gleam_catRADEC.append((catalog['catalog'][i]['RA'],catalog['catalog'][i]['DEC']))
    gleam_catI.append(catalog['catalog'][i]['flux']['I'][0])

gleam_catRADEC = np.array(gleam_catRADEC)
gleam_catI = np.array(gleam_catI)

### Do a RA/DEC cut to only look at relevant sources ###
maxRA = 1.1*np.max(decon_RADEC[:,0])
minRA = .9*np.min(decon_RADEC[:,0])
print 'Min/Max RA: ',str(minRA)+'/'+str(maxRA)

maxDEC = .9*np.max(decon_RADEC[:,1])
minDEC = 1.1*np.min(decon_RADEC[:,1])
print 'Min/Max DEC: ',str(minDEC)+'/'+str(maxDEC)

cutRA = gleam_catRADEC[gleam_catRADEC[:,0] < maxRA]
cutI = gleam_catI[gleam_catRADEC[:,0] < maxRA]
cutRA = cutRA[cutRA[:,0] > minRA]
cutI = cutI[cutRA[:,0] > minRA]
print len(cutRA)


cutRADEC = cutRA[cutRA[:,1] < maxDEC]
cutI = cutI[cutRA[:,1] < maxDEC]
cutRADEC = cutRADEC[cutRADEC[:,1] > minDEC]
cutI = cutI[cutRADEC[:,1] > minDEC]
final_cat_fov = np.copy(cutRADEC)
final_cat_I = np.copy(cutI)

dRA = []
dDec = []
fluxI = []
ct=0
for (ra,dec) in decon_RADEC:
    idx=angulardist(final_cat_fov,final_cat_I,ra,dec,decon_I[ct])
    dx,dy=final_cat_fov[idx]
    fluxI.append(final_cat_I[idx])
    dRA.append(dx-ra)
    dDec.append(dy-dec)
    ct+=1

pl.scatter(dRA,dDec)
pl.show()
pl.plot(fluxI,decon_I,'.')
pl.show()

from matplotlib  import cm
fig = pl.figure(figsize=(6,6))
ax = fig.add_subplot(111)
print np.shape(final_cat_fov)
ax.scatter(final_cat_fov[:,0],final_cat_fov[:,1],s=20,marker='.',c=final_cat_I,cmap=cm.jet)
ax.scatter(decon_RADEC[:,0],decon_RADEC[:,1],s=20,marker='o',c=decon_I,cmap=cm.jet)
pl.show()

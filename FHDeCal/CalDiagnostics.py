import numpy as np
import pyuvdata
import sys
from glob import glob
import pylab as pl
import matplotlib.gridspec as gridspec

#gs = gridspec.GridSpec(12, 12)
def fit(data):
    frqs = np.linspace(0,np.pi,1024)
    amps = np.linspace(0.01,2.*np.max(data),100)
    modes = np.linspace(0.01,30.,100)
    MSE = np.zeros((100,100))
    ct_m = 0
    for m in modes:
        ct_a = 0
        for a in amps:
            MSE[ct_m,ct_a] = np.sum(np.abs(data - a*np.sin(m*frqs)))
            ct_a+=1
        ct_m+=1
    min_mode,min_amp = np.argwhere(np.min(MSE)==MSE)[0]
    print min_mode,min_amp
    sinfit = amps[min_amp]*np.sin(modes[min_mode]*frqs)
    return sinfit

    

### Give it FHD directory and find calibrations

fhd_dir = sys.argv[1]
'Looking for appropriate FHD calibration files.'

calsav = glob(fhd_dir+'/calibration/*_cal.sav')[0]
obssav = glob(fhd_dir+'/metadata/*_obs.sav')[0]
settingsfile = glob(fhd_dir+'/metadata/*_settings.txt')[0]

fhdcals = pyuvdata.uvcal.UVCal()
fhdcals.read_fhd_cal(cal_file=calsav,obs_file=obssav,settings_file=settingsfile,raw=True)

ant_inds = np.sum(np.angle(fhdcals.gain_array[:,0,:,0,0]),1) > .0
good_ants = fhdcals.ant_array[ant_inds]
gains = fhdcals.gain_array
frqs = np.linspace(100,200,1024)
gparrsz = (int(np.floor(np.sqrt(len(good_ants)))),int(np.ceil(len(good_ants)/np.floor(np.sqrt(len(good_ants))))))

sq_ants = np.zeros((gparrsz[0]*gparrsz[1]),dtype=int)
sq_ants[:len(good_ants)] = good_ants
sq_ants = sq_ants.reshape(gparrsz[0],gparrsz[1])

gain_sums = np.sum(np.abs(gains[:,0,:,0,0]),1)
gain_std = np.std(np.sum(np.abs(gains[:,0,:,0,0]),1))

print sq_ants
fig,ax = pl.subplots(gparrsz[0],gparrsz[1],sharex='all', sharey='all')
#fig.set_size_inches(10,10)
for i in range(gparrsz[0]):
    for j in range(gparrsz[1]):
        if np.sum(np.angle(gains[sq_ants[i,j],0,:,0,0])) > .0:
            #ax[i,j].set_title(str(sq_ants[i,j]+1))
            ax[i,j].plot(frqs,np.abs(gains[sq_ants[i,j],0,:,0,0]),'.',markersize=1)
            ax[i,j].xaxis.set_major_locator(pl.MaxNLocator(3))
            ax[i,j].yaxis.set_major_locator(pl.MaxNLocator(3))
            pl.xlim(120,180)
            good_ant = np.abs(gain_sums[sq_ants[i,j]] - np.mean(gain_sums)) < gain_std
            if good_ant:
                ax[i,j].annotate(str(sq_ants[i,j]),xy=(.65,.1),xycoords='axes fraction')
            else:
                ax[i,j].annotate(str(sq_ants[i,j]),xy=(.65,.1),xycoords='axes fraction',color='r')
        else:
            ax[i,j].annotate(str(sq_ants[i,j]),xy=(.65,.1),xycoords='axes fraction',color='r')
            #title = ax[i,j].set_title(str(sq_ants[i,j]+1))
            #pl.setp(title,color='r')
#pl.tight_layout()
pl.subplots_adjust(bottom=0.04,top=.96,left=.04,right=.96,hspace=.1)
pl.show()



print 'Plotting GLOBAL PHASEPASS!'
gblbpass = np.mean(np.abs(gains[:,0,:,0,0]),0)
### Fit only where there's data ###
frqs_fit = np.linspace(120,180,818-205)
abs_fit = np.poly1d(np.polyfit(frqs_fit,np.abs(gains[14,0,205:818,0,0]),1))#fit(gblphs)


gain_sums = np.sum(np.abs(gains[:,0,:,0,0]),1)
gain_std = np.std(np.sum(np.abs(gains[:,0,:,0,0]),1))

#pl.hist(gain_sums,50)
#pl.axvline(np.median(gain_sums),0,10)
#pl.show()

pl.subplot(211)
for i in good_ants:
    print np.sum(np.angle(gains[i-1,0,:,0,0]))
    if np.sum(np.angle(gains[i-1,0,:,0,0])) > 0.0 :
        if np.abs(gain_sums[i-1] - np.mean(gain_sums)) > gain_std:
            pl.plot(frqs,np.abs(gains[i-1,0,:,0,0]),'--')
        else:
            pl.plot(frqs,np.abs(gains[i-1,0,:,0,0]),'.')
#pl.plot(frqs,gblphs_fit(frqs),'--')
### Normalize the fit ###
gains14 = abs_fit(frqs)/np.max(abs_fit(frqs)[205:818])

pl.subplot(212)
pl.plot(frqs,np.abs(gains[14,0,:,0,0]),label='Dish 14 Gains')
pl.plot(frqs,gains14,label='Gain Fit')
pl.plot(frqs,gains14*gblbpass,'--',label='Fit*GlobalBpass')
pl.legend()
#pl.plot(frqs,np.angle(gains[14,0,:,0,0])*np.arcsin(gblphs_fit),'--')
pl.show()

print 'Global BPASS and Polyfit Residuals'
pl.plot(frqs,np.abs(gains[14,0,:,0,0])-gains14*gblbpass,'.')
pl.show()



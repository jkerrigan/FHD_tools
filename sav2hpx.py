import numpy as np
import healpy as hp
from glob import glob
import json

NSIDE=128
bm_freq_arr = []
beam_files = np.sort(glob('./HERABeams/HERA - E-pattern - *MHz.txt'))
#freq_arr = np.linspace(1e8,2e8,101)
freq_arr = []
bm_ct=0
for beam in beam_files:
    print beam
    freq = float(beam.split(' ')[4].split('MHz.txt')[0])*1e6

    if freq <= 99.*1e6 or freq >= 201.*1e6:
        print 'Skipped.'
        continue
    else:
        print freq
    freq_arr.append(freq)
    bmtxt = np.loadtxt(beam,skiprows=2)
    Et = bmtxt[:,3]*np.exp(-1j*np.radians(bmtxt[:,4]))
    Et = bmtxt[:,5]*np.exp(-1j*np.radians(bmtxt[:,6]))
    norm = np.sqrt(np.max((Et**2) + (Ep**2)))
    theta_rad = bmtxt[:,0]*np.pi/180.
    phi_rad = bmtxt[:,1]*np.pi/180.
    m=np.zeros(hp.nside2npix(NSIDE))
    pix=hp.ang2pix(NSIDE,theta_rad,phi_rad)
    m[pix] = Et/norm#bmtxt[:,2]
    bm_freq_arr.append(m)
    bm_ct+=1

#freq_arr = np.array(freq_arr)
bm_freq_arr = np.array(bm_freq_arr).T
print np.shape(bm_freq_arr)
np.savetxt('HERAPol100-200MHz.txt',bm_freq_arr)

move2idl = {}
move2idl['n_side']=NSIDE
move2idl['healpix_ordering']=list(pix)
move2idl['n_hpx']=hp.nside2npix(NSIDE)
move2idl['hera_frequency_array']=list(freq_arr)
print np.shape(freq_arr)
with open('CombHERABMkeys.txt','w') as outfile:
    json.dump(move2idl, outfile)

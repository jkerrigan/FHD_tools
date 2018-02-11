import numpy as np
import pyuvdata
from glob import glob
import sys
import os


### We're going to use xx as the container                                                                                                             

class PullandCombine:
    
    def __init__(self,mfile):
        self.mfile = mfile
        self.prefix = ('.').join(mfile.split('.')[0:3])
        self.suffix = ('.').join(mfile.split('.')[4:])
        ### Only pulling xx and yy
        self.npol = 2
        self.polarization_array = np.array([-5,-6]) #,-7,-8])

    def pullData(self,pol):
        uv = pyuvdata.miriad.Miriad()
        print self.prefix+'.'+pol+'.'+self.suffix
        uv.read_miriad(self.prefix+'.'+pol+'.'+self.suffix)
        print 'Polarization '+pol+' Loaded.'
        if pol == 'xx':
            self.dim = np.shape(uv.data_array)
            self.data_array = np.zeros((self.dim[0],self.dim[1],self.dim[2],self.npol),dtype=complex)
            self.flag_array = np.zeros((self.dim[0],self.dim[1],self.dim[2],self.npol),dtype=bool)
            self.nsample_array = np.zeros((self.dim[0],self.dim[1],self.dim[2],self.npol))
            self.data_array[:,:,:,0] = uv.data_array[:,:,:,0]
            self.flag_array[:,:,:,0] = uv.flag_array[:,:,:,0]
            self.nsample_array[:,:,:,0] = uv.nsample_array[:,:,:,0]
        elif pol == 'yy':
            self.data_array[:,:,:,1] = uv.data_array[:,:,:,0]
            self.flag_array[:,:,:,1] = uv.flag_array[:,:,:,0]
            self.nsample_array[:,:,:,1] = uv.nsample_array[:,:,:,0]
        elif pol == 'xy':
            self.data_array[:,:,:,2] = uv.data_array[:,:,:,0]
            self.flag_array[:,:,:,2] = uv.flag_array[:,:,:,0]
            self.nsample_array[:,:,:,2] = uv.nsample_array[:,:,:,0]
        elif pol == 'yx':
            self.data_array[:,:,:,3] = uv.data_array[:,:,:,0]
            self.flag_array[:,:,:,3] = uv.flag_array[:,:,:,0]
            self.nsample_array[:,:,:,3] = uv.nsample_array[:,:,:,0]
        del(uv)

    def combineWrite(self,uvfits=False):
        uv = pyuvdata.miriad.Miriad()
        uv.read_miriad('./'+self.prefix+'.xx.'+self.suffix)
        uv.Npols=self.npol
        uv.data_array=np.copy(self.data_array)
        uv.flag_array=np.copy(self.flag_array)
        uv.nsample_array=np.copy(self.nsample_array)
        uv.polarization_array=self.polarization_array
        del(self.data_array)
        del(self.flag_array)
        del(self.nsample_array)
        if uvfits:
            uv.write_uvfits(self.prefix+'.'+self.suffix+'.uvfits',spoof_nonessential=True,force_phase=True)
        else:
            uv.write_miriad(self.prefix+'.'+self.suffix)


pol_arr = ['xx','yy']#,'xy','yx']
#files = ['zen.2458042.50580.xx.HH.uvOR']
files = sys.argv[1:]
for f in files:
    print f
    if os.path.isfile(('.').join(f.split('.')[:3])+'.HH.uvOR.uvfits'):
        print 'File exists.'
        continue
    PTG = PullandCombine(f)
    for p in pol_arr:
        PTG.pullData(p)
    PTG.combineWrite(uvfits=True)

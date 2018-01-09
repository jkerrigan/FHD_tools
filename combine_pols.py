import numpy as np
import pyuvdata
from glob import glob

directory='/users/jkerriga/data/shared/HERA_new/IDR1/'
### We're going to use xx as the container                                                                                                                            
uvxx = pyuvdata.miriad.Miriad()
uvxx.read_miriad(directory+'zen.2458042.59528.xx.HH.uvOR')
print 'Loaded.'
uvyy = pyuvdata.miriad.Miriad()
uvyy.read_miriad(directory+'zen.2458042.59528.yy.HH.uvOR')
print 'Loaded.'
uvxy = pyuvdata.miriad.Miriad()
uvxy.read_miriad(directory+'zen.2458042.59528.xy.HH.uvOR')
print 'Loaded.'
uvyx = pyuvdata.miriad.Miriad()
uvyx.read_miriad(directory+'zen.2458042.59528.yx.HH.uvOR')
print 'Loaded.'

npol=4
dim = np.shape(uvxx.data_array)
data_array = np.zeros((dim[0],dim[1],dim[2],4),dtype=complex)
data_array[:,:,:,0] = uvxx.data_array[:,:,:,0]
data_array[:,:,:,1] = uvyy.data_array[:,:,:,0]
data_array[:,:,:,2] = uvxy.data_array[:,:,:,0]
data_array[:,:,:,3] = uvxx.data_array[:,:,:,0]


flag_array = np.zeros((dim[0],dim[1],dim[2],4),dtype=bool)
flag_array[:,:,:,0] = uvxx.flag_array[:,:,:,0]
flag_array[:,:,:,1] = uvyy.flag_array[:,:,:,0]
flag_array[:,:,:,2] = uvxy.flag_array[:,:,:,0]
flag_array[:,:,:,3] = uvxx.flag_array[:,:,:,0]

nsample_array = np.zeros((dim[0],dim[1],dim[2],4))
nsample_array[:,:,:,0] = uvxx.nsample_array[:,:,:,0]
nsample_array[:,:,:,1] = uvyy.nsample_array[:,:,:,0]
nsample_array[:,:,:,2] = uvxy.nsample_array[:,:,:,0]
nsample_array[:,:,:,3] = uvxx.nsample_array[:,:,:,0]

polarization_array = np.array([-5,-6,-7,-8])

uvxx.Npols=npol
uvxx.data_array=data_array
uvxx.flag_array=flag_array
uvxx.nsample_array=nsample_array
uvxx.polarization_array=polarization_array

uvxx.write_uvfits(directory+'zen.2458042.59528.HH.uvOR.uvfits',spoof_nonessential=True,force_phase=True)

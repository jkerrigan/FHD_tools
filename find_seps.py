import numpy as np
import pyuvdata
import sys
import matplotlib as mpl
mpl.use('Agg')
import pylab as pl

f = sys.argv[1]

uv = pyuvdata.miriad.Miriad()
uv.read_miriad(f)

bsl = []
seps = []
for a1 in uv.antenna_numbers:
    idx1 = a1 == uv.antenna_numbers
    for a2 in uv.antenna_numbers:
        idx2 = a2 == uv.antenna_numbers
        if np.sqrt(np.sum((uv.antenna_positions[idx1,1] - uv.antenna_positions[idx2,1])**2)) < 15.:
            seps.append(np.sqrt(np.sum((uv.antenna_positions[idx1,0] - uv.antenna_positions[idx2,0])**2)))
            bsl.append((a1,a2))
seps = np.array(seps).reshape(-1)
bsl = np.array(bsl)
bins = np.linspace(0.,130,50)
#print bins
#print np.shape(bsl)
#print np.sum(np.digitize(seps,bins)==np.unique(np.digitize(seps,bins))[1])
### find closest bin to 14m
bsl14 = np.argmin((bins - 14.)**2)-1
   
antpairs = bsl[np.digitize(seps,bins)==np.unique(np.digitize(seps,bins))[bsl14]]
pairSeps = seps[np.digitize(seps,bins)==np.unique(np.digitize(seps,bins))[bsl14]]

format_pairs = []

xpos = uv.antenna_positions[:,0]
ypos = uv.antenna_positions[:,1]
#print pairSeps
#print 'Max sep: ',np.max(pairSeps),' Min sep: ',np.min(pairSeps)
pl.figure()
pl.plot(xpos,ypos,'.')
for ap in antpairs:
    a1 = str(ap[0])
    a2 = str(ap[1])
    idx1 = ap[0] == uv.antenna_numbers
    idx2 =  ap[1] == uv.antenna_numbers
#    print xpos[idx1][0],ypos[idx1][0]
    pl.arrow(xpos[idx1][0],ypos[idx1][0],xpos[idx2][0]-xpos[idx1][0],ypos[idx2][0]-ypos[idx1][0],head_width=2,length_includes_head=True)
    format_pairs.append(('_').join((a1,a2)))
#pl.savefig('EWBaselines.png')
print (',').join(format_pairs)    

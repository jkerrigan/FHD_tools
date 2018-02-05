bm_hpx = READ_ASCII('HERAPol100-200MHz.txt')
bm_keys = JSON_PARSE('CombHERABMkeys.txt',/toarray)
help,bm_keys

hera_beam_hpx=bm_hpx.field001
healpix_ordering='RING'
n_hpx=ulong(bm_keys['n_hpx'])
hera_frequency_array=float(bm_keys['hera_frequency_array'])
nside=uint(bm_keys['n_side'])

undefine,bm_hpx
undefine,bm_keys

save, /variables, filename = 'HERA_Pol_X_128.sav'

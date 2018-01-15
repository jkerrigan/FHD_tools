# FHD_tools

Preparation for FHD:

combine_pols.py - FHD seems to require all 4 polarizations (or perhaps just 'xx' and 'yy') for full deconvolution. This script combines individual HERA polarization miriad files into a single uvfits with forced phasing.

match_sources.py - This script attempts to compare sources found through FHD's deconvolution to a known source catalog (GLEAM). It does this by finding the shortest euclidean distance in a normalized RA, DEC, and Flux space between the FHD source and all catalog sources. Catalog sources can exceed 300k potential sources and are thus pruned before attempting a match by limiting to the observation FoV.
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import healpy as hp
import pandas as pd

import classes as cs


hdul = fits.open("/Users/DanielBautista/21 cm Cosmology/GLEAM_EGC_v2.fits")
frame = pd.DataFrame(hdul[1].data) # max sources is 307455

t = cs.Catalog(frame,5)


flux = t.flux("int_flux_151") #total = 3072
ra = t.RA
dec = t.DEC

#print(type(t.frame))
print()

print(t.frame)
#k_alpha = t.kAlpha()
#print(k_alpha)

'''
alt, az = t.altaz(np.pi/4)

print(alt)
print(az)
print("\n\n")

for i in range(len(alt)):
    print(t.position_vector(alt[i],az[i]))
'''

#flux = t.frame.int_flux_151 #total = 307455
'''
total = 0
for item in flux:
    total += 1
    print(item)'''

'''
print(flux)
print()
print(t.DEC)
print()
print(t.RA)
#print(type(flux))
#print(total)
'''

'''
print(type(t.RA))

for item in t.DEC:
    print(item)

plt.figure()
plt.scatter(frame.RAJ2000, frame.int_flux_076)
plt.show()

flux = t.flux()

time = np.linspace(0, 2*np.pi, 307455)

alt, az = t.altaz(time)

print("alt:", alt)
print("az:", az)
'''

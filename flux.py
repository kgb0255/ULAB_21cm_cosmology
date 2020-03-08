import numpy as np
from Catalog import altaz


def kAlpha(flux_1, flux_2, freq_1, freq_2):
        """
        return an array of k and alphas
        first column is k for all sources and second column is a for all sources
        """
        a = np.log(flux_1/flux_2)/np.log(freq_1/freq_2)
        k = flux_1 / np.power(freq_1, a)
        return k, a

def get_flux(k, alpha, freqs):
    return [k*freq**(alpha) for freq in freqs]

def find_brightest(ra, dec, times):
    alt, az = altaz(ra,dec, times)
    indices = np.where(alt*180/np.pi > 40)
    return indices[1]


def get_gleam_flux_ra_dec(df, freqs, times, num):
    d = df.sort_values(by = "int_flux_151", ascending=False)
    d = d.dropna(axis = 0, how = "any")
    
    RA = np.asarray(d.RAJ2000)
    DEC = np.asarray(d.DEJ2000) 
    
    sources = find_brightest(RA, DEC, times)
    RA, DEC = RA[sources], DEC[sources] 

    d = d.iloc[sources]
    orgFrame = d[[col for col in d.keys() if ((col=='RAJ2000' or col=='DEJ2000'or col[:9]=='int_flux_') and col!= 'int_flux_fit_200') and col != 'int_flux_wide']][:num]
    
    orgFreqMHz = [(int) (col[10:]) for col in orgFrame.keys() if (col[:9]=='int_flux_')]
    flux_1 = np.array(orgFrame['int_flux_151'])
    flux_2 = np.array(orgFrame['int_flux_227'])
    freq_1, freq_2 = 151, 227
    k, alpha = kAlpha(flux_1, flux_2, freq_1, freq_2)

    return np.array(get_flux(k, alpha, freqs)), RA[:num], DEC[:num]

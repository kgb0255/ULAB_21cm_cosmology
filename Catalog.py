import numpy as np
from scipy.constants import c


class Catalog():

    def __init__(self,name, ra, dec, flux, time, freqs, lat = 37.875*np.pi/180):
        """
        Initializes the Catalog and makes a new Pandas DataFrame containing
        the Right Ascension and Declination as well as all the fluxes

        Parameters:
        df = Pandas DataFrame
        num = sample size num
        time = time range array
        freqs= freq array
        Creates:
        self.orgFrame as Pandas DataFrame type, cleaned, all orginal data, with size num
        self.flux as np array type, cleaned, contains only sample size num and freq freqs
        self.RA = right ascencion from J2000 in degrees as numpy.ndarray
        self.DEC = declination from J2000 in degrees as numpy.ndarray
        self.orgFreqMHz = all old freq in order as in df passed in
        self.FreqMHz = array of all freq run
        self.time = array of all time run
        self.altaz = [alt, az] for each source for each time
        self.kAlphas = first row is k and second row is alpha for all sources

        Functions:
        get_flux(self, freq) return an array of flux at Freq
        getAltazAtFreq(self, freq) return an array of [alt, az] at Freq
        kAlpha(self) return a size 2 array with first being k of all sources and second being alphas
        position_vectors()
        """
       
        self.ra      = ra
        self.dec     = dec
        self.flux    = flux
        self.time    = time
        self.freqMHz = freqs

        
        self.alt, self.az  = altaz(ra, dec, time, lat)
        self.s_vectors     = self.position_vector()



        

    def position_vector(self):
        """
        Calculates the position vector to a source in the sky
        Parameters:
        alt = the altitude of the source from the horizon, given in radians
        az  = the angle from north, moving towards the east, given in radians
        Returns
        vector in cartesian coordinates [x,y,z] as a numpy.ndarray
        """
        x = np.cos(self.alt) * np.cos(self.az)
        y = np.cos(self.alt) * np.sin(self.az)
        z = np.sin(self.alt)
        ##vector = np.array([x,y,z])
        return np.array([x, y, z])

   
    def getPhase(self,b):
        """return an array phase factors with number of row being number of source,
        number of column being number of freq"""
        arr_source = np.exp(-2*np.pi*1.0j*np.einsum('k,ijl->ljk', self.freqMHz*1e6/c, np.einsum('ijk, i->ijk',self.s_vectors, b)))
        return arr_source
    
    
    
def altaz(ra, dec, time, rad = False, lat = 37.875*np.pi/180):
    """
    modified from from Max
    Calculates Altitude and Azimuth at given times, centered at HERA
    parameters:
    time = lst in radian
    ra = Right ascension of the star in degrees or radians
    dec = Declination of the star in degrees or radians
    rad = True if RA and DEC are in radian or False if RA and DEC are in degree
    returns:
    Returns alt, and az all in radian
    """

    PI = np.pi
    alt = []
    az = []
    #Setting the latitude/longitude of HERA
    if rad == False:
        ra =ra * PI/180
        dec =dec * PI/180
    for t in time:
        #Converts the LST to hour angle
        hour_array = np.mod((t - ra), 2*PI)

        #Calculates the Altitude and Azimuth
        alt.append( np.arcsin(np.sin(dec)*np.sin(lat)
                        + np.cos(dec)*np.cos(lat)*np.cos(hour_array)))
        az.append(np.arctan2(np.sin(hour_array)*np.cos(dec),
                        np.cos(hour_array)*np.cos(dec)*np.sin(lat) - np.sin(dec)*np.cos(lat)) + PI)

    array = []

    return np.array(alt), np.array(az)

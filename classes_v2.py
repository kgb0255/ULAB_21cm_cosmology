import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
import astropy
import healpy as hp
import scipy.constants as spc
import time
import math

class Catalog():
    
    def __init__(self, df, num, time = np.linspace(0, 2*np.pi, 768)):
        """
        modified from James and Daniel's code
        Initializes the Catalog and makes a new Pandas DataFrame containing the Right Ascension and Declination as well as all the fluxes
        
        Parameters:
        df = Pandas DataFrame
        num = sample size
        time = time range array

        Creates: 
        self.frame as Pandas DataFrame type
        self.RA = right ascencion from J2000 in degrees as numpy.ndarray
        self.DEC = declination from J2000 in degrees as numpy.ndarray
        self.freqMHz = all possible freq in order as in df passed in
        self.time = time
        self.ALTAZ = array row size is the same as time array size, 
                        each each contains the array of [alt, az] 
                        for each freq in oder of self.freqMHz
        self.kAlphas = each row is a source, each row contains[k, alpha]
        
        Functions:
        getFluxAtFreq(self, freq) return an array of flux at Freq
        getAltazAtFreq(self, freq) return an array of [alt, az] at Freq
        kAlpha(self)
        position_vectors()
        """
        d = df.sort_values(by = "int_flux_076", ascending=False)
        d = d.dropna(axis = 0, how = "any")
        self.frame = d[[col for col in d.keys() if ((col=='RAJ2000' or col=='DEJ2000'or col[:9]=='int_flux_') 
                                                      and col!= 'int_flux_fit_200') and col != 'int_flux_wide']]
        self.frame = self.frame[:num]
       
        self.RA = np.asarray(self.frame.RAJ2000)
        self.DEC = np.asarray(self.frame.DEJ2000)
        """array of all possible freq"""
        self.freqMHz = [(int) (col[10:]) for col in self.frame.keys() 
                        if (col[:9]=='int_flux_')]
        self.time = time
        self.ALTAZ = [self.altaz(t) for t in time]
        self.kAlphas = self.kAlpha()     
        self.s_vectors = [[self.position_vector(source[0], source[1])for source in t] for t in self.ALTAZ]
    
    def altaz(self, time, rad = False, lat = 37.875*np.pi/180):
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
        ra = self.RA
        dec = self.DEC
        PI = np.pi
        #Setting the latitude/longitude of HERA
        if rad == False:
            ra =ra * PI/180
            dec =dec * PI/180
        
        #Converts the LST to hour angle
        hour_array = np.mod((time - ra), 2*PI)
    
        #Calculates the Altitude and Azimuth
        alt = np.arcsin(np.sin(dec)*np.sin(lat)
                        + np.cos(dec)*np.cos(lat)*np.cos(hour_array))
        az = np.arctan2(np.sin(hour_array)*np.cos(dec),
                        np.cos(hour_array)*np.cos(dec)*np.sin(lat) - np.sin(dec)*np.cos(lat)) + PI
        
        array = []
        for alti, azi in zip(alt, az):
            array.append([alti, azi])
            
        return array
    
    def getFluxAtFreq(self, freq):
        """return a flux array frequency FREQ"""
        assert np.where(self.freqMHz==freq)
        var = "int_flux_"
        if freq<100:
            var = var + '0' + str(freq)
        else:
            var = var + str(freq)
        return np.asarray(self.frame[var])
    
    def getAltazAtFreq(self, freq):
        """return an altaz array for at FREQ"""
        assert np.where(self.freqMHz==freq)
        index = 0
        currFreq = self.freqMHz[0]
        while currFreq != freq:
            index += 1 
            currFreq = self.freqMHz[index]
        return [t[index] for t in self.ALTAZ]
    
    def kAlpha(self):
        """
        return an array of k and alphas
        each row is one source that contains [k, a]
        """
        frame_just_flux = np.array(self.frame[
            [col for col in self.frame.keys() if (col[:9]=='int_flux_')]])
        array = []
        for source in frame_just_flux:
            #find alpha
            flux1 = source[0]
            flux2 = source[1]
            v1 = self.freqMHz[0]
            v2 = self.freqMHz[1]
            a = math.log(flux1/flux2, v2/v1)
            #find k
            k = flux1 / math.pow(v1, a)
            array.append([k, a])
        return array
    
    def position_vector(self, alt, az):
        """
        Calculates the position vector to a source in the sky 
        
        Parameters: 
        alt = the altitude of the source from the horizon, given in radians            
        az  = the angle from north, moving towards the east, given in radians
        
        Returns
        vector in cartesian coordinates [x,y,z] as a numpy.ndarray
        """
        x = np.cos(alt) * np.cos(az)
        y = np.cos(alt) * np.sin(az)
        z = np.sin(alt)            
        vector = np.asarray([x,y,z])
        return vector
   
    def get_phase(self, b):
        """return an array phase factors with number of row being number of source, 
        number of column being number of freq"""       
        arr_source = []
        for si, bi in zip(self.s_vectors, b):
            arr_freq = []
            for freq in self.freqMHz:
                arr_freq.append(np.exp(-2*np.pi*1.j*freq/spc.c*np.dot(bi, si)))
            arr_source.append(arr_freq)
        return arr_source

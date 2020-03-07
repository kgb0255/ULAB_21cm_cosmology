# need to make data reduction a separate method, so that 
#   flux() is not needed to organize data

'''
make a catalog class: methods:
- def altaz()
- def flux()

class antenna
- def beam()
- def phase()
'''

import numpy as np
import pandas as pd


class Catalog:
    """
    Data type that will take care of the data reduction and repetitive calculations of things such as the alt/az and flux of the sources

    Methods:
    flux, altaz
    """
    def __init__(self, frame, num_stars):
        """
        Initializes the Catalog and makes a new Pandas DataFrame containing the Right Ascension and Declination as well as all the fluxes
        
        Parameters:
        frame = Pandas DataFrame
        num_stars = the number of stars in your sample

        Creates: 
        self.frame as Pandas DataFrame type
        self.RA = right ascencion from J2000 in radians as numpy.ndarray
        self.DEC = declination from J2000 in radians as numpy.ndarray
        """
        df = frame
        new_frame = [col for col in df.columns if ('int_flux' in col or "RAJ2000" in col or "DEJ2000" in col) and "err" not in col]
        new_frame = frame[new_frame]

        star_number = num_stars
        
        # drop the NaN values that we don't want
        new_frame = new_frame.dropna(axis=0, how="any")

        # sort the columns by increasing flux
        new_frame = new_frame.sort_values(by="int_flux_wide")

        # create a frame with num_stars largest fluxes
        self.frame = new_frame.iloc[len(new_frame)-star_number:]
        
        #pick out the right ascension and declination for the stars with the largest fluxes
        frame = self.frame
        self.RA = np.asarray(frame.RAJ2000) * np.pi/180
        self.DEC = np.asarray(frame.DEJ2000)* np.pi/180
        
    def flux(self, frequency): 
        """
        Picks out the brightest fluxes in the gleam catalog in the frequency range
        
        Parameters:
        frequency = the frequency of fluxes to be returned 

        Creates:
        self.flux = largest fluxes in the sky as np.ndarray

        returns:
        gleam flux specified range as an np.ndarray
        """
        max_frame = self.frame
        # create self.flux variable for specified frequency to be numpy array containing largest fluxes
        try:
            self.flux = np.asarray(getattr(max_frame,frequency))
            return self.flux
        except:
            print("Here are the valid frequencies:")
            print(np.asarray(max_frame.columns)) 

    def altaz(self, time, rad = True, lat=37.875*np.pi/180):
        """
        From Max :) 
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
            ra =ra* PI/180
            dec =dec*PI/180
    
        #Converts the LST to hour angle
        hour_array = np.mod((time - ra), 2*PI)
    
        #Calculates the Altitude and Azimuth
        alt = np.arcsin(np.sin(dec)*np.sin(lat)+np.cos(dec)*np.cos(lat)*np.cos(hour_array))
        az = np.arctan2(np.sin(hour_array)*np.cos(dec), np.cos(hour_array)*np.cos(dec)*np.sin(lat)-np.sin(dec)*np.cos(lat))+PI
    
        return alt, az

    def position_vector(self, alt, az):
        '''
        Calculates the position vector to a source in the sky 

        Parameters: 
        alt = the altitude of the source from the horizon, given in radians
        az  = the angle from north, moving towards the east, given in radians

        Returns:
        vector in cartesian coordinates [x,y,z] as a numpy.ndarray
        '''
        x = np.cos(alt) * np.cos(az)
        y = np.cos(alt) * np.sin(az)
        z = np.sin(alt)
        vector = np.asarray([x,y,z])
        return vector

    def phase(self, baseline): # needs a baseline vector 
        pass#return np.exp(-2*np.pi*1.j*freq/spc.c*np.dot(b, s))

    def kAlpha(self):
        fluxes = [col for col in self.frame.columns if "flux" in col and "wide" not in col]
        print(type(self.frame))

    def kAlpha_andrea(self):
        """return sourcesize * 2 array where each row is one source and the first column is k, second column is a"""
        frame_just_flux = np.array(self.frame[[col for col in self.frame.keys() if (col[:9]=='int_flux_')]])
        array = []
        for source in frame_just_flux:
            #find alpha
            flux1 = source[0]
            flux2 = source[1]
            v1 = self.freqMHz[0]
            v2 = self.freqMHz[1]
            a = np.log(flux1/flux2, v2/v1)
            #find k
            k = flux1 / np.pow(v1, a)
            array.append([k, a])
        return array
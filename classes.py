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


class Catalog:
    """
    Data type that will take care of the data reduction and repetitive calculations of things such as the alt/az and flux of the sources

    Methods:
    flux, altaz
    """
    def __init__(self, frame):
        """
        Initializes the Catalog and makes a new Pandas DataFrame containing the Right Ascension and Declination as well as all the fluxes
        
        Parameters:
        frame = Pandas DataFrame

        Creates: 
        self.frame as Pandas DataFrame type
        self.RA = right ascencion from J2000 in degrees as numpy.ndarray
        self.DEC = declination from J2000 in degrees as numpy.ndarray
        """
        df = frame
        new_frame = [col for col in df.columns if ('int_flux' in col or "RAJ2000" in col or "DEJ2000" in col) and "err" not in col]
        self.frame = frame[new_frame]
        self.RA = np.asarray(frame.RAJ2000)
        self.DEC = np.asarray(frame.DEJ2000)

    def flux(self, num_stars):
        """
        Picks out the brightest fluxes in the gleam catalog in the 151 MHz range
        
        Parameters:
        num_stars = the number of stars in your sample

        Creates:
        self.flux = largest fluxes in the sky as np.ndarray

        returns:
        gleam flux in 151 MHz range as an np.ndarray
        """
        star_number = num_stars
        new_frame = self.frame
        
        # drop the NaN values that we don't want
        new_frame = new_frame.dropna(axis=0, how="any")

        # sort the columns by increasing flux
        new_frame = new_frame.sort_values(by="int_flux_wide")

        # create a frame with num_stars largest fluxes
        max_frame = new_frame.iloc[len(new_frame)-star_number:]
        
        # create self.flux variable to be numpy array containing largest fluxes
        self.flux = np.asarray(max_frame.int_flux_151)
        return self.flux


    def altaz(self, time, rad = False, lat=37.875*np.pi/180):
        """
        Calculates Altitude and Azimuth at given times, centered at HERA
    
        parameters: 
        time = lst in radian
        ra = Right ascension of the star in degrees or radians
        dec = Declination of the star in degrees or radians
        rad = True if RA and DEC are in radian or False if RA and DEC are in degree
        
        Note: time and RA/DEC need to have the same size
        
        Note 2: time array needs to have index of 307455 to work for now. Important!
    
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
# need to make data reduction a separate method, so that 
#   flux() is not needed to organize data

'''
make a catalog class: methods:
- def altaz()
- def flux()
- def phase()

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
        """
        df = frame
        new_frame = [col for col in df.columns if ('int_flux' in col or "RAJ2000" in col or "DEJ2000" in col) and "err" not in col]
        self.frame = frame[new_frame]

    def flux(self):
        """
        Picks out the fluxes in the gleam catalog in the 151 MHz range
        also picks out and stores the right ascension and declination of the sources in units of degrees

        Parameters:
        none so far, but am open to suggestions

        returns:
        gleam flux in 151 MHz range as an np.ndarray
        """
        star_number = 3072
        frame = self.frame
        new_frame = [col for col in frame.columns if ("int_flux" in col or "RAJ2000" in col or "DEJ2000" in col and "err" not in col)]
        new_frame = frame[new_frame]

        # drop the NaN values that we don't want
        new_frame = new_frame.dropna(axis=0, how="any")

        # sort the columns by increasing flux
        new_frame = new_frame.sort_values(by="int_flux_wide")

        # create a frame with the 1000 largest fluxes
        max_frame = new_frame.iloc[len(new_frame)-star_number:]
        self.frame = max_frame

        self.RA = np.asarray(frame.RAJ2000)
        self.DEC= np.asarray(frame.DEJ2000)
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



class Antenna:

    def __init__(self):
        pass
    def beam(self):
        pass

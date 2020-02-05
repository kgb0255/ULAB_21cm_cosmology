# Here is a file where I will be testing how to use github
# I have added the file to git so now it is being tracked
#print("hello world")

# now I need to find a way to upload this file to git 

# did it work?

'''
make a catalog class: methods:
- def altaz()
- def flux()
- def phase()

class antenna
- def beam()
- def phase()
'''

class Catalog:
    def __init__(self, frame):
        self.frame = frame
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


    def altaz(time, rad = False, lat=37.875*np.pi/180):
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


    def flux()
        self.flux = np.asarray(max_frame.int_flux_151)
        return self.flux


class Antenna:
    def beam()

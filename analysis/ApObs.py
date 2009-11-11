import numpy as np


class Aperture(object):
    """Aperture object"""
    def __init__(self, num):
        """Create lists and values"""
        object.__init__(self)
        self.num = num
        self.xcoord = []
        self.ycoord = []
        self.sky = []
        self.flux = []
        self.errors = []
        self.mag = []

    def addLine(self, line):
        """Add data into object in the form:
            xcoordinate
            ycoordinate
            sky value
            flux value
            mag-errors
            magniture"""
        self.xcoord.append(float(line[0]))
        self.ycoord.append(float(line[1]))
        self.sky.append(float(line[2]))
        self.flux.append(float(line[3]))
        self.errors.append(float(line[4]))
        self.mag.append(float(line[5]))


    def coords(self):
        """Returns the coordinates in a 2-tuple"""
        return self.xcoord, self.ycoord

    def getErrors(self):
        """Returns the errors on the flux, as scaled
        by the errors in magnitude"""
        ar_err = np.array(self.errors)
        ar_mag = np.array(self.mag)
        ar_flux = np.array(self.flux)


        return list(ar_flux * ar_err / ar_mag)

    def xyscatter(self):
        """Returns 2-tuple of x and y offsets from the average 
        coordinate"""
        x = np.array(self.xcoord)
        y = np.array(self.ycoord)
        self.xav = np.average(self.xcoord) * np.ones(x.shape)
        self.yav = np.average(self.ycoord) * np.ones(y.shape)

        return list(x - self.xav), list(y - self.yav)


    def stats(self):
        """Returns the average and standard deviation"""
        return np.average(self.flux), np.std(self.flux)

    def residuals(self):
        av = self.stats()[0] * np.ones(np.shape(self.flux))
        return self.flux - av



    #end of class definition



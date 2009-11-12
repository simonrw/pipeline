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

    def smoothListGaussian(self, degree=2):
        """Gaussian smoothing function
        credit: http://www.swharden.com/blog/2008-11-17-linear-data-smoothing-in-python/"""
        window=degree*2-1
        weight=np.array([1.0]*window)
        weightGauss=[]
        for i in range(window):
            i=i-degree+1
            frac=i/float(window)
            gauss=1/(np.exp((4*(frac))**2))
            weightGauss.append(gauss)
        weight=np.array(weightGauss)*weight
        smoothed=[0.0]*(len(self.flux)-window)
        for i in range(len(smoothed)):
            smoothed[i]=sum(np.array(self.flux[i:i+window])*weight)/sum(weight)
        return smoothed


    #end of class definition


def aperComp(aplist):
    """Arguments: 
        list or dictionary of apertures
    Returns:
        Average counts per aperture
        SD per aperture"""
    counts = []
    err = []
    if type(aplist) == list:
        for aper in aplist:
            av, er = aper.stats()
            counts.append(av)
            err.append(er)
    elif type(aplist) == dict:
        for aper in aplist.itervalues():
            av, er = aper.stats()
            counts.append(av)
            err.append(er)

    counts = np.array(counts)
    err = np.array(err)

    return counts, err

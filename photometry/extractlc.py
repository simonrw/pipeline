#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from numpy import array, arange
import matplotlib.pyplot as plt
#from IPython.Shell import IPShellEmbed

class Aperture(object):
    def __init__(self, num):
        self.num = num
        self.xcoord = []
        self.ycoord = []
        self.sky = []
        self.flux = []
        self.errors = []
        self.mag = []

    def addLine(self, line):
        self.xcoord.append(float(line[0]))
        self.ycoord.append(float(line[1]))
        self.sky.append(float(line[2]))
        self.flux.append(float(line[3]))
        self.errors.append(float(line[4]))
        self.mag.append(float(line[5]))


    def subtracted(self):
        sky = array(self.sky)
        flux = array(self.flux)
        return list(flux - sky)

    def coords(self):
        return self.xcoord, self.ycoord

    def getErrors(self):
        ar_err = array(self.errors)
        ar_mag = array(self.mag)
        ar_flux = array(self.flux)


        return list(ar_flux * ar_err / ar_mag)


def getAperNumbers(fl, d):
    """Arguments:
        fl = filelist, list of strings containing 
                filenames
        d = dir, directory where fl is

    Returns:
        list of numbers of apertures"""


    t = open(d + '/' + fl[0])
    tmp = t.readlines()
    t.close()

    nums = []

    for line in tmp:
        if '#' not in line:
            nums.append(line.split()[0])

    return nums

def main(dir):


    dir = dir.rstrip('/')

    filelist = os.listdir(dir)

    aperNums = getAperNumbers(filelist, dir)

    
    




    aperlist = {}


    for i in aperNums:
        aperlist[i] = Aperture(i)





    for file in filelist:
        fptr = open(dir + '/' + file)
        data = []



        for line in fptr.readlines():
            if '#' not in line:
                data.append(line.rstrip('\n'))

        for line in data:
            vals = line.split()
            num = vals[0] 
            coords = float(vals[1]), float(vals[2])
            flux = {'sky': float(vals[5]), 'aper': float(vals[6])}
            err = float(vals[4])
            mag = float(vals[3])

            aperlist[num].addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))
            #if num == 1:
            #    ap1.addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))
            #elif num == 2:
            #    ap2.addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))
            #elif num == 3:
            #    ap3.addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))
            #elif num == 4:
            #    ap4.addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))
            #elif num == 5:
            #    ap5.addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))
    

    #for aper in [ap1, ap2, ap3, ap4, ap5]:
    #    plt.subplot(5, 1, aper.num)
    #    if aper.num == 1:
    #        plt.title('Lightcurves')
    #    plt.xlabel('Frame')
    #    plt.ylabel(r'$f_{aperture} - f_{sky}$')
    #    plt.plot(aper.subtracted())
    #plt.show()
    for aper in aperlist.itervalues():
        plt.figure(aper.num)
        plt.subplot(411)
        plt.title('Lightcurve for object %s' % aper.num)
        plt.xlabel('Frame')
        plt.ylabel(r'$f_{aperture} - f_{sky}$')
        #plt.plot(aper.sky, 'bx')
        plt.errorbar(arange(len(filelist)), aper.flux, yerr = aper.getErrors(),  fmt='bx')

        plt.subplot(412)
        plt.ylabel('Sky')
        plt.plot(aper.sky, 'rx')

        plt.subplot(413)
        plt.ylabel('X')
        plt.plot(aper.xcoord, 'go')
        plt.subplot(414)
        plt.ylabel('Y')
        plt.plot(aper.ycoord, 'go')

    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Program usage: %s <dir>" % sys.argv[0]
        exit(1)
    main(sys.argv[1])


#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import numpy as np
import matplotlib.pyplot as plt
#from IPython.Shell import IPShellEmbed

class Aperture(object):
    def __init__(self, num):
        self.num = num
        self.xcoord = []
        self.ycoord = []
        self.sky = []
        self.flux = []

    def addLine(self, line):
        self.xcoord.append(float(line[0]))
        self.ycoord.append(float(line[1]))
        self.sky.append(float(line[2]))
        self.flux.append(float(line[3]))


    def subtracted(self):
        sky = np.array(self.sky)
        flux = np.array(self.flux)
        return list(flux - sky)

    def coords(self):
        return self.xcoord, self.ycoord

    def rav(self, binsize):
        self.data = np.array(self.subtracted())

        runningav = []
        for i in range(binsize/2., len(self.data) - binsize/2.):
            for j in range(-binsize/2., binsize/2.):
                av = 


def main(dir):


    dir = dir.rstrip('/')

    filelist = os.listdir(dir)

    ap1 = Aperture(1)
    ap2 = Aperture(2)
    ap3 = Aperture(3)
    ap4 = Aperture(4)
    ap5 = Aperture(5)


    for file in filelist:
        fptr = open(dir + '/' + file)
        data = []
        for line in fptr.readlines():
            if '#' not in line:
                data.append(line.rstrip('\n'))

        for line in data:
            vals = line.split()
            num = int(vals[0])
            coords = float(vals[1]), float(vals[2])
            flux = {'sky': float(vals[5]), 'aper': float(vals[6])}

            if num == 1:
                ap1.addLine((coords[0], coords[1], flux['sky'], flux['aper']))
            elif num == 2:
                ap2.addLine((coords[0], coords[1], flux['sky'], flux['aper']))
            elif num == 3:
                ap3.addLine((coords[0], coords[1], flux['sky'], flux['aper']))
            elif num == 4:
                ap4.addLine((coords[0], coords[1], flux['sky'], flux['aper']))
            elif num == 5:
                ap5.addLine((coords[0], coords[1], flux['sky'], flux['aper']))

    ap1.rav(10)
    #for aper in [ap1, ap2, ap3, ap4, ap5]:
    #    plt.figure(aper.num)
    #    plt.title('Lightcurve for object %d' % aper.num)
    #    plt.xlabel('Frame')
    #    plt.ylabel(r'$f_{aperture} - f_{sky}$')
    #    plt.plot(aper.subtracted())
    #plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Program usage: %s <dir>" % sys.argv[0]
        exit(1)
    main(sys.argv[1])


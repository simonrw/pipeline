#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import numpy as np
import matplotlib.pyplot as plt



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

    def xyscatter(self):
        x = np.array(self.xcoord)
        y = np.array(self.ycoord)
        self.xav = np.average(self.xcoord) * np.ones(x.shape)
        self.yav = np.average(self.ycoord) * np.ones(y.shape)

        return list(x - self.xav), list(y - self.yav)


    


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

    for aper in [ap1, ap2, ap3, ap4, ap5]:
        plt.figure(aper.num)
        plt.subplot(211)
        plt.plot(aper.xcoord, 'rx')
        plt.subplot(212)
        plt.plot(aper.ycoord, 'rx')
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Program usage: %s <dir>" % sys.argv[0]
        exit(1)
    main(sys.argv[1])


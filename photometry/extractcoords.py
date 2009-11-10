#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import numpy as np
import matplotlib.pyplot as plt
from ApObs import Aperture




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

    for aper in aperlist.itervalues():
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


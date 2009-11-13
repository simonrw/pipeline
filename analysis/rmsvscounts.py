#!/usr/bin/env python2.5

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from numpy import array, arange
import matplotlib.pyplot as plt
from ApObs import Aperture, aperComp
#from IPython.Shell import IPShellEmbed


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

def main(args):
    dir = args.rstrip('/')
    filelist = os.listdir(dir)
    filelist.remove('cmd')
    aperNums = getAperNumbers(filelist, dir)
    # create dictionary of apertures
    aperlist = {} 
    for i in aperNums:
        aperlist[i] = Aperture(i)




    # read in data to aperture objects
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

    #plt.plot(aperlist['3'].smoothListGaussian(10), 'r-')
    #plt.plot(aperlist['3'].flux, 'bx')
    #plt.show()
    counts, rms = aperComp(aperlist)
    plt.plot(counts, rms, 'rx')

    plt.show()


if __name__ == '__main__':


    main(sys.argv[1])


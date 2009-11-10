#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from numpy import array, arange
import matplotlib.pyplot as plt
from ApObs import Aperture
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

def main(options, args):


    dir = args[0].rstrip('/')

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

     
    if options.coords and not options.lc and not options.hist:
        for aper in aperlist.itervalues():
            plt.figure(aper.num)
            plt.subplot(211)
            plt.title('Coordinates')
            plt.plot(aper.xcoord, 'rx')
            plt.subplot(212)
            plt.plot(aper.ycoord, 'rx')

    elif options.lc and not options.coords and not options.hist:
        for aper in aperlist.itervalues():
            plt.figure(aper.num)
            plt.subplot(211)
            plt.title('Lightcurve for object %s' % aper.num)
            plt.xlabel('Frame')
            plt.ylabel(r'$f_{aperture} - f_{sky}$')
            #plt.plot(aper.sky, 'bx')
            plt.errorbar(arange(len(filelist)), aper.flux, yerr = aper.getErrors(),  fmt='bx')

            plt.subplot(212)
            plt.ylabel('Sky')
            plt.plot(aper.sky, 'rx')
    
    elif options.lc and options.coords and not options.hist:
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

    elif options.hist:
        bins = raw_input('How many bins?  ')
        for aper in aperlist.itervalues():
            plt.figure(aper.num)
            plt.title('Distribution for aperture %s' % aper.num)
            plt.xlabel('Counts')
            plt.ylabel('Frequency')
            plt.hist(aper.flux, int(bins))


    elif options.err:
        for aper in aperlist.itervalues():
            plt.figure(aper.num)
            plt.title('Error scatter plot for aperture %s' % aper.num)
            plt.xlabel('Counts')
            plt.ylabel('Error in counts')
            plt.scatter(aper.flux, aper.getErrors())

    plt.show()

if __name__ == '__main__':

    parser = OptionParser(usage="usage: %prog [options] <dir>", conflict_handler="resolve",
            version="0.1")

    parser.add_option('-c', '--coords', action="store_true",
            dest='coords', default=False, help="Print extracted coordinates")

    parser.add_option('-l', '--lc', action="store_true", 
            dest="lc", default=False, help="Print extracted lightcurves")

    parser.add_option('-h', '--hms', action="store_true", 
            dest="hist", default=False, help="Print extracted histogram")

    parser.add_option('-e', '--errors', action="store_true", 
            dest="err", default=False, help="Print extracted errors")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "Program usage: %s [options] <dir>" % sys.argv[0]
        exit(1)
    
    if not options.lc and not options.coords and not options.hist and not options.err:
        parser.error("""No plot commands supplied,
            -l/--lc = lightcurves
            -c/--coords = coords
            -h/--hist = histogram
            -e/-errors = errors""")


    main(options, args)


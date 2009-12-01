#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import matplotlib.pyplot as plt
import numpy as np
#from IPython.Shell import IPShellEmbed


class Aperture(object):
    def __init__(self, number=0, xpos=-1, ypos=0, flag=255):
        object.__init__(self)
    
        #set up defaults
        self._number = int(number)
        self._xpos = float(xpos)
        self._ypos = float(ypos)
        self._flag = int(flag)

    def number(self):
        return self._number

    def xpos(self):
        return self._xpos

    def ypos(self):
        return self._ypos

    def flag(self):
        return self._flag

    def __str__(self):
        return "%d %f %f %d" % (self._number,
                self._xpos,
                self._ypos,
                self._flag)


def main((options, args)):
    try:
        f = open(args[0])
    except IOError, message:
        print >> sys.stderr,  message
        exit(1)

    aplist = []
    radiusval = 2.0

    for line in f.readlines():
        if '#' not in line:
            try:
                num, x, y, fl = line.strip().split()
            except ValueError:
                print >> sys.stderr, "Error: incorrect file format\nExiting..."
                sys.exit(1)
            aplist.append(Aperture(number=num,
                xpos=x,
                ypos=y,
                flag=fl))
    
    f.close()
    
    bad = 0
    good = 0

    print "Converting with threshold value %s" % options.thresh

    header = """# 1 NUMBER
# 2 X_IMAGE
# 3 Y_IMAGE
# 4 FLAGS
"""


    outputfile = open(options.output, mode="w")
    outputfile.write(header)

    for aper in aplist:
        if aper.flag() <= int(options.thresh):
            string = "%d %f %f 0.0 0.0 0.0 0.0 ? %f 0.0 0.0 annulus circle\n" % (aper.number(),
                    aper.xpos(), aper.ypos(), radiusval)
            outputfile.write(string)
            string = "#ANN %d 1.77 3.79\n" % (aper.number())
            outputfile.write(string)
            good += 1
        else:
            bad += 1

    print "%d apertures rejected" % bad
    print "%d apertures accepted" % good

    
    outputfile.close()

if __name__ == '__main__':


    usage = "Usage: %prog [options] file"
    parser = OptionParser(usage=usage, version="0.1")

    parser.add_option('-t', '--threshold', action='store', dest='thresh', 
            default=4, help="Maximum flag value to include", metavar="f")

    parser.add_option("-o", "--output", action="store", dest="output",
            default="output.dat", help="Output file", metavar="file")

    options, args = parser.parse_args()

    if not len(args):
        print >> sys.stderr, "usage: %s [options] file" % sys.argv[0]
        exit(1)
    
    main((options, args))

#!/usr/bin/env python2.5

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from astLib import astImages
import pylab 
import pyfits
#from IPython.Shell import IPShellEmbed


def main(arg):
    dir = arg[1].rstrip('/')
    p = Popen("ls %s" % dir, shell=True, stdout=PIPE)
    filelist = p.communicate()[0].split()
    filelist.remove('cmd')









if __name__ == '__main__':

    if len(sys.argv) != 2:
        print >> sys.stderr, "Program usage: %s dir" % sys.argv[0]
        exit(1)


    main(sys.argv)


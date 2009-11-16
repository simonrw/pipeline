#!/usr/bin/env python2.5

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from astLib import astImages
from jg.subs import progressbarClass
import pyfits
import time
#from IPython.Shell import IPShellEmbed


def main(arg):
    dir = arg[1].rstrip('/')
    p = Popen("ls %s" % dir, shell=True, stdout=PIPE)
    filelist = p.communicate()[0].split()

    pb = progressbarClass(len(filelist))

    outputdir = '/tmp/movies/'

    for i, file in enumerate(filelist):
        if 'iKon' in file:
            try:
                hdulist = pyfits.open(dir + '/' + file)
            except:
                print >> sys.stderr, "Error opening file %s" % (dir + '/' + file)
                exit(1)

            header = hdulist[0].header
            imdata = hdulist[0].data

            hdulist.close()

            size = int(header['naxis1']) * int(header['naxis2'])
            cutLevels = ["smart", 99.5]

            stub = file.split('.')[0]
            outputFileName = outputdir + stub + '.png'
            colorMapName = 'hot'

            astImages.saveBitmap(outputFileName, imdata, cutLevels, size, colorMapName)
            pb.progress(i) 


    command = ('mencoder',
               'mf://%s*.png' % outputdir,
               '-mf',
               'type=png:w=1024:h=1024:fps=10',
               '-ovc',
               'lavc',
               '-lavcopts',
               'vcodec=mpeg4',
               '-oac',
               'copy',
               '-o',
               'output.avi')

    os.spawnvp(os.P_WAIT, 'mencoder', command)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print >> sys.stderr, "Program usage: %s dir" % sys.argv[0]
        exit(1)

    tstart = time.time()
    main(sys.argv)
    print 'Time taken: %f min' % ((time.time() - tstart) / 60.)


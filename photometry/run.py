#!/usr/bin/env python
#important parameters

from subprocess import Popen, PIPE, STDOUT
from sys import argv, stderr, exit
import os
from optparse import OptionParser
from srw import progressbarClass, fitsDir, _mkdir
from time import time

def printoutput(txt):
        print "Running command\n"
        print txt
        print



def main((options, args)):#

    parameters = {
            "biasle": "0",
            "centro": "true",
            "exsource": "constant",
            "etime": "1.0",
            "fixann": "false",
            "usemags": "false",
            "maxiter": "9",
            "maxshift": options.maxshift,
            "optima": "false",
            "padu": "1.2",
            "photon": "1",
            "positive": "true",
            "sature": "1.7E30",
            "search": options.search,
            "skyest": "2",
            "toler": "0.05",
            "usemask": "false"
            }

    srcdir = fitsDir(args[0])
    outputdir = options.opdir.rstrip('/')

    #check if options.opdir is a directory
    try:
        _mkdir(outputdir)
    except (OSError, c):
        print >> stderr, "Error: %s" % c
        exit(1)

    try:
        paramfile = open(outputdir + "/.cmd", mode="w")
    except IOError:
        print >> stderr, "Error writing parameters to %s" % ('/'.join((outputdir, 'cmd')))
        exit(1)

    #make parameter file read only
    p = Popen('chmod -w %s/.cmd' % outputdir, shell=True)
    p.communicate()

    for pair in parameters.iteritems():
        paramfile.write(" = ".join(pair) + "\n")

    paramfile.close()

    if not os.path.isfile(options.apfile):
        print >> stderr, "Error: initial aperture file '%s' must exist in current directory" % options.apfile
        exit(1)




    if not options.verbose:
        pb = progressbarClass(len(srcdir))

    for i, file in enumerate(srcdir):
        stub = file.rpartition('/')[2]
        sdf = stub.rstrip('.fits') + ".sdf"
        catfile = stub.partition('.')[0] + ".cat"
        cmd = 'source $STARLINK_DIR/etc/profile && convert && fits2ndf in=\"%s/%s\" out=\"%s/%s\"' % (srcdir, stub, srcdir, stub.partition('.')[0])
        if options.verbose:
            printoutput(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        result, error = p.communicate()
        if len(error) != 0:
            print error

        #check for apfile existence
        if not os.path.isfile(options.apfile):
            print >> stderr, "Error: initial aperture file '%s' must exist in current directory" % options.apfile
            exit(1)

        cmd = 'source $STARLINK_DIR/etc/profile && photom && autophotom'
        cmd += ' in=%s/%s infile=%s outfile=%s/%s' % (srcdir, sdf, options.apfile, outputdir, catfile)
        for n, v in parameters.iteritems():
            cmd += ' ' + '='.join((n, v))
        if options.verbose:
            printoutput(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        result, error = p.communicate()

        if len(error) != 0:
            print error

        cmd = 'rm %s && cp %s/%s %s' % (options.apfile, outputdir, catfile, options.apfile)
        if options.verbose:
            printoutput(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        result, error = p.communicate()

        if len(error) != 0:
            print error

        cmd = 'rm -f %s/%s' % (srcdir, sdf)
        if options.verbose:
            printoutput(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        result, error = p.communicate()

        if len(error) != 0:
            print error

        if not options.verbose:
            pb.progress(i)

if __name__ == "__main__":

    parser = OptionParser(usage='Program usage: %prog [options] dir', version='0.1',
            conflict_handler="resolve")

    defsearch = '12'
    defshift = '20'

    parser.add_option('-a', '--apfile', action='store', dest='apfile', default='apertures.dat',
            help='Initial aperture file for photometry', metavar='file')

    parser.add_option('-o', '--output', action='store', dest='opdir', default='./output',
            help='Dir to place output files', metavar='dir')

    parser.add_option('-v', '--verbose', action="store_true", dest="verbose", default=False,
            help="Print extra information")

    parser.add_option('-s', '--search', action='store', dest='search', default=defsearch,
            help='Centroiding search box, default %s' % (defsearch))

    parser.add_option('-m', '--maxshift', action='store', dest='maxshift', default=defshift,
            help='Maximum shifting, default %s' % (defshift))


    options, args = parser.parse_args()


    if len(args) != 1:
        print >> stderr, "Program requires directory"
        exit(1)

    tstart = time()
    main((options, args))
    print "\n\nTime taken: %f min" % ((time() - tstart) / 60.)

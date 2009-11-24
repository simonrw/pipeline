#!/usr/bin/env python2.6
#important parameters
parameters = {
        "biasle": "0",
        "centro": "true",
        "exsource": "constant",
        "etime": "1.0",
        "fixann": "false",
        "usemags": "false",
        "maxiter": "9",
        "maxshift": "9",
        "optima": "false",
        "padu": "1.2",
        "photon": "1",
        "positive": "true",
        "sature": "1.7E30", 
        "search": "10",
        "skyest": "2",
        "toler": "0.05",
        "usemask": "false"
        }

from subprocess import Popen, PIPE, STDOUT, call
from sys import argv, stderr, exit
import os
from optparse import OptionParser
from modules import progressbarClass, fitsDir, _mkdir
from time import time

def printoutput(txt):
        print "Running command\n"
        print txt
        print



def main((options, args)):#

    srcdir = args[0].rstrip('/')
    outputdir = options.opdir.rstrip('/')

    #check if options.opdir is a directory
    try:
        _mkdir(outputdir)
    except OSError as c:
        print >> stderr, "Error: %s" % c
        exit(1)

    try:
        paramfile = open(outputdir + "/.cmd", mode="w")
    except IOError:
        print >> stderr, "Error writing parameters to %s" % ('/'.join(outputdir, 'cmd'))
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

    p = Popen('ls %s/*.fits' % srcdir, shell=True, stdout=PIPE, stderr=PIPE)
    result, error = p.communicate()


    filelist = []
    for file in result.split():
        filelist.append(file)

    if not options.verbose:
        pb = progressbarClass(len(filelist))

    for i, file in enumerate(filelist):
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
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        cmd = 'rm %s && cp %s/%s %s' % (options.apfile, outputdir, catfile, options.apfile)
        if options.verbose:
            printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        cmd = 'rm -f %s/%s' % (srcdir, sdf)
        if options.verbose:
            printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        if not options.verbose:
            pb.progress(i)

if __name__ == "__main__":

    parser = OptionParser(usage='Program usage: %prog [options] dir', version='0.1',
            conflict_handler="resolve")


    parser.add_option('-a', '--apfile', action='store', dest='apfile', default='apertures.dat',
            help='Initial aperture file for photometry', metavar='file')

    parser.add_option('-o', '--output', action='store', dest='opdir', default='./output',
            help='Dir to place output files', metavar='dir')
    
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose", default=False,
            help="Print extra information")
    

    options, args = parser.parse_args()


    if len(args) != 1:
        print >> stderr, "Program requires directory"
        exit(1)

    tstart = time()
    main((options, args))
    print "\n\nTime taken: %f min" % ((time() - tstart) / 60.)

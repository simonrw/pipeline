#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT, call
from sys import argv, stderr, exit
import os
from optparse import OptionParser

def printoutput(txt):
        print "Running command\n"
        print txt
        print

def _mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
        
        credit: http://code.activestate.com/recipes/82465/
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

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

def main((options, args)):

    srcdir = args[0].rstrip('/')
    outputdir = options.opdir

    #check if options.opdir is a directory
    try:
        _mkdir(outputdir)
    except OSError as c:
        print >> stderr, "Error: %s" % c
        exit(1)

    try:
        paramfile = open(outputdir + "/cmd", mode="w")
    except IOError:
        print >> stderr, "Error writing parameters to %s" % ('/'.join(outputdir, 'cmd'))
        exit(1)


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


    for file in filelist:
        stub = file.rpartition('/')[2]
        sdf = stub.rstrip('.fits') + ".sdf"
        catfile = stub.partition('.')[0] + ".cat"
        cmd = 'source $STARLINK_DIR/etc/profile && convert && fits2ndf in=\"%s/%s\" out=\"%s/%s\"' % (srcdir, stub, srcdir, stub.partition('.')[0])
        printoutput(cmd)
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        result, error = p.communicate()
        if len(error) != 0:
            print error
        cmd = 'source $STARLINK_DIR/etc/profile && photom &&  autophotom in=%s/%s infile=%s outfile=%s/%s biasle=0 centro=true exsource=constant etime=1.42 fixann=false usemags=false maxiter=9 maxshift=9 optima=false padu=1.2 photon=1 positive=true sature=1.7E30 search=10 skyest=2 toler=0.05 usemask=false' % (srcdir, sdf, options.apfile, outputdir, catfile)
        printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        cmd = 'rm %s && cp %s/%s %s' % (options.apfile, outputdir, catfile, options.apfile)
        printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        cmd = 'rm -f %s/%s' % (srcdir, sdf)
        printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

if __name__ == "__main__":

    parser = OptionParser(usage='Program usage: %prog [options] dir', version='0.1',
            conflict_handler="resolve")


    parser.add_option('-a', '--apfile', action='store', dest='apfile', default='apertures.dat',
            help='Initial aperture file for photometry', metavar='file')

    parser.add_option('-o', '--output', action='store', dest='opdir', default='./output',
            help='Dir to place output files', metavar='dir')

    

    options, args = parser.parse_args()


    if len(args) != 1:
        print >> stderr, "Program requires directory"
        exit(1)

    main((options, args))


#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT, call
from sys import argv, stderr, exit
from os import environ
from os import path
from optparse import OptionParser

def printoutput(txt):
        print "Running command\n"
        print txt
        print


def main(args):

    srcdir = args[1].rstrip('/')
    outputdir = 'output'

    if not path.isfile('apertures.dat'):
        print >> stderr, "Error: file 'apertures.dat' must exist in current directory"
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
        cmd = 'source $STARLINK_DIR/etc/profile && photom &&  autophotom in=%s/%s infile=apertures.dat outfile=%s/%s biasle=0 centro=true exsource=constant etime=1.42 fixann=false usemags=false maxiter=9 maxshift=9 optima=false padu=1.2 photon=1 positive=true sature=1.7E30 search=10 skyest=2 toler=0.05 usemask=false' % (srcdir, sdf, outputdir, catfile)
        printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        cmd = 'rm apertures.dat && cp %s/%s ./apertures.dat' % (outputdir, catfile)
        printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

        cmd = 'rm -f %s/%s' % (srcdir, sdf)
        printoutput(cmd)
        p = call(cmd, shell=True, stdout=PIPE, stderr=STDOUT)

if __name__ == "__main__":
    if len(argv) != 2:
        print >> stderr, "Program requires directory"
        exit(1)

    main(argv)


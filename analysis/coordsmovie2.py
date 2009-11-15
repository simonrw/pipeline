#!/usr/bin/env python

import sys
import os
import matplotlib.pyplot as plt
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import numpy as np
import time
#from IPython.Shell import IPShellEmbed


def main(options, args):
    plt.ion()
    datadir = args[0].rstrip('/')
    p = Popen('ls %s' % datadir, shell=True, stdout=PIPE)
    files = p.communicate()[0]
    files = files.split()
    files.remove('cmd')


    fig = plt.figure()
    ax = fig.add_subplot(111)
    tstart = time.time()

    f = open(datadir + '/' + files[0])
    xcoords = []
    ycoords = []
    for pltline in f:
        words = pltline.split()
        xcoords.append(words[1])
        ycoords.append(words[2])
    f.close()
    plt.title('Frame 1')
    line, = ax.plot(xcoords, ycoords, 'ro')

    

    for i, file in enumerate(files[1:]):
        f = open(datadir + '/' + file)
        xcoords = []
        ycoords = []
        for pltline in f:
            if '#' not in pltline:
                words = pltline.split()
                xcoords.append(words[1])
                ycoords.append(words[2])

        f.close()
        plt.title('Figure %d' % i)
        line.set_xdata(xcoords)
        line.set_ydata(ycoords)

        fig.canvas.draw()


    

if __name__ == '__main__':

    parser = OptionParser()

    options, args = parser.parse_args()
    main(options, args)


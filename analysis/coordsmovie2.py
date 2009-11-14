#!/usr/bin/env python2.5

import sys
import os
import matplotlib.pyplot as plt
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
#from IPython.Shell import IPShellEmbed


def main(options, args):
    plt.ion()
    datadir = args[0].rstrip('/')
    files = os.listdir(datadir)
    files.remove('cmd')

    f = open(datadir + '/' + files[0])
    xcoords = []
    ycoords = []

    for line in f.readlines():
        if '#' not in line:
            words = line.split()
            xcoords.append(words[1])
            ycoords.append(words[2])

    pltline, = plt.plot(xcoords, ycoords, 'ro', markersize=20, markerfacecolor='white')
    plt.axis([0, 1024, 0, 1024])
    plt.title('Frame 1')


    for i, file in enumerate(files[1:]):
        f = open(datadir + '/' + file)
        xcoords = []
        ycoords = []
        for line in f:
            if '#' not in line:
                words = line.split()
                xcoords.append(words[1])
                ycoords.append(words[2])

        f.close()
        pltline.set_xdata(xcoords)
        pltline.set_ydata(ycoords)
        plt.title('Frame %d' % i)
        plt.draw()


if __name__ == '__main__':

    parser = OptionParser()

    options, args = parser.parse_args()
    main(options, args)


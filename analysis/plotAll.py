#!/usr/bin/env python
# encoding: utf-8
"""
analyse.py

Created by Simon Walker on 2009-12-16.
Copyright (c) 2009 University of Warwick. All rights reserved.
"""

import sys
import getopt
import numpy as np
import matplotlib.pyplot as plt
from optparse import OptionParser
import srw



def main((options, args)):

    ap = int(args[0])

    if options.lc:
        lc = srw.extractSingle(options.lc)[ap]

    if options.nonflat:
        nf = srw.extractSingle(options.nonflat)[ap]

    if options.nonflat and options.lc:
        diff = lc - nf
        ratio = lc / nf

    if options.coords:print coordsData.shape
exit(0)

        coords = srw.extractSingleCoords(options.coords)[ap]


        x = coords[0]
        y = coords[1]

    if options.error:
        er = srw.extractSingle(options.error)[ap]

    if options.sky:
        sk = srw.extractSingle(options.sky)[ap]

    if options.zd:
        zd = np.loadtxt(options.zd)

    # Plot the data

    fig = plt.figure()

    length = np.arange(len(lc))


    # list of what to plot and what formatting and label
    # - data
    # - format
    # - label

    plots = []

    #try:
    #    plots.append([residuals, 'rx', r'$f_i - \bar{f}$'])
    #except UnboundLocalError:
    #    pass


    try:
        plots.append([nf, 'rx', 'Non-flatted lightcurve'])
    except UnboundLocalError:
        pass

    try:
        plots.append([diff, 'bx', r'$f_{\mathrm{flat}} - f_{\mathrm{nonflat}}'])
    except UnboundLocalError:
        pass
    try:
        plots.append([ratio, 'bx', r'$f_{\mathrm{flat}} / f_{\mathrm{nonflat}}'])
    except UnboundLocalError:
        pass

    try:
        plots.append([sk, 'gx', 'Sky counts'])
    except UnboundLocalError:
        pass

    try:
        plots.append([x, 'b.', 'X coordinate (pix)'])
    except UnboundLocalError:
        pass

    try:
        plots.append([y, 'b.', 'Y coordinate (pix)'])
    except UnboundLocalError:
        pass

    try:
        plots.append([zd, 'rx', 'Zenith distance'])
    except UnboundLocalError:
        pass







    no_plots = len(plots) + 1

    ax = fig.add_subplot(no_plots, 1, 1)
    try:
        ax.errorbar(length, lc, er, fmt='rx')
    except UnboundLocalError:
        ax.plot(lc, 'rx')

    ax.set_title('Information for aperture %d' % ap)
    ax.set_ylabel('Counts')

    for val in range(2, len(plots) + 2):
        ax = fig.add_subplot(no_plots, 1, val)
        ax.plot(plots[val-2][0], plots[val-2][1])
        ax.set_ylabel(plots[val-2][2])



    #ax = fig.add_subplot(812)
    #ax.plot(residuals, 'rx')
    #ax.set_ylabel(r'$f_i - \bar{f}$')

    #ax = fig.add_subplot(813)
    #ax.plot(nf, 'bx')
    #ax.set_ylabel('Non-flatted lightcurve')

    #ax = fig.add_subplot(814)
    #ax.plot(diff, 'rx')
    #ax.set_ylabel(r'$f_{\mathrm{flat}} - f_{\mathrm{nonflat}}')

    #ax = fig.add_subplot(815)
    #ax.plot(ratio, 'rx')
    #ax.set_ylabel(r'$f_{\mathrm{flat}} / f_{\mathrm{nonflat}}')

    #
    #ax = fig.add_subplot(816)
    #ax.plot(sk, 'bx')
    #ax.set_ylabel('Sky counts')
    #
    #ax = fig.add_subplot(817)
    #ax.plot(x, 'gx')
    #ax.set_ylabel('X coordinate (pix)')
    #
    #ax = fig.add_subplot(818)
    #ax.plot(y, 'gx')
    #ax.set_ylabel('Y coordinate (pix)')
    #ax.set_xlabel('Frame')

    plt.show()



if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option('-l', '--lightcurve', action='store', dest='lc',
            help='Lightcurve file', metavar='f')

    parser.add_option('-c', '--coords', action='store', dest='coords',
            help='Coordinates', metavar='f')


    parser.add_option('-e', '--error', action='store', dest='error',
            help='Errors', metavar='f')

    parser.add_option('-s', '--sky', action='store', dest='sky',
            help='Sky', metavar='f')

    parser.add_option('-n', '--nonflat', action='store', dest='nonflat',
            help='Pre-flatted data', metavar='f')

    parser.add_option('-z', '--zd', action='store', dest='zd',
            help='Zenith distance', metavar='z')

    options, args = parser.parse_args()


    if not options.lc and not options.coords and not options.zd and not options.sky and not options.nonflat and not options.error:
        print >> sys.stderr, "At least one of [lcesnz] required"
        exit(1)


    if not options.lc:
        print >> sys.stderr, "Lightcurve data required"
        exit(1)




    if len(args) != 1:
        print >> sys.stderr, "Aperture number required"
        exit(1)

    main((options, args))


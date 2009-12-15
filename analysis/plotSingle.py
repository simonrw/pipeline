#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys

def main(args):
    
    usage = "Program usage: %s <file> <ap>" % args[0]

    try:
        file = open(args[1])
    except IndexError:
        print >> sys.stderr, usage
        exit(1)

    header = file.readlines()[0]
    file.close()

    aps = np.array(header.strip().split()[1:])

    
    ldata = np.loadtxt('lightcurve.extract')
    try:
        plt.plot(ldata[:, aps == args[2]], 'rx')
    except IndexError:
        print >> sys.stderr, usage
        exit(1)

    plt.title('Lightcurve for aperture %s' % args[2])
    plt.xlabel('Frame')
    plt.ylabel('Counts')
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

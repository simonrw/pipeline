#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys
import srw


def main(args):
    
    usage = "Program usage: %s <file> <ap>" % args[0]

    data = srw.extractSingle(args[1])
    info = data[args[2]]
    
   
    
    if info is not None:
        try:
            plt.plot(info, 'rx')
        except IndexError:
            print >> sys.stderr, usage
            exit(1)

        plt.title('Lightcurve for aperture %s' % args[2])
        plt.xlabel('Frame')
        plt.ylabel('Counts')
        plt.show()
    

if __name__ == '__main__':
    main(sys.argv)

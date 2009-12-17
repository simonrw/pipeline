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
import srw



def main(ap):
    
    ap = int(ap)
    
    try:
        lc = srw.extractSingle('lightcurve.extract')[ap]
    except Exception, e:
        raise e
        
    
    try:
        coords = srw.extractSingleCoords('coords.extract')[ap]
    except Exception, e:
        raise e

    
    x = coords[0]
    y = coords[1]
    
    
    try:
        er = srw.extractSingle('error.extract')[ap]        
    except Exception, e:
        raise e
        
    
    try:
        sk = srw.extractSingle('sky.extract')[ap]
    except Exception, e:
        raise e
        
    
    # Plot the data
    
    fig = plt.figure()
    
    length = np.arange(len(lc))
    
    

    ax = fig.add_subplot(411)
    ax.errorbar(length, lc, er, fmt='rx')
                
    ax.set_title('Information for aperture %d' % ap)
    ax.set_ylabel('Counts')
    
    ax = fig.add_subplot(412)
    ax.plot(sk, 'bx')
    ax.set_ylabel('Counts')
    
    ax = fig.add_subplot(413)
    ax.plot(x, 'gx')
    ax.set_ylabel('X coordinate (pix)')
    
    ax = fig.add_subplot(414)
    ax.plot(y, 'gx')
    ax.set_ylabel('Y coordinate (pix)')
    ax.set_xlabel('Frame')
    
    plt.show()
    


if __name__ == "__main__":
    print """
Warning: this program requires 4 files in the current directory:

- lightcurve.extract:   flux data
- error.extract:        errors data
- coords.extract:       coordinate data
- sky.extract:          sky background data

"""
    try:
        main(sys.argv[1])
    except IndexError:
        print >> sys.stderr, "Program usage: %s <ap number>" % sys.argv[0]
        sys.exit(1)

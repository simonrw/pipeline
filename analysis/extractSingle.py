#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys
from optparse import OptionParser
import srw

def main(options, args):
    try:
        dir = args[0]
    except IndexError:
        print >> sys.stderr, "Directory argument required"
        
    datadir = srw.dataDir(dir)
    
  
    
    selected = []

    for file in datadir.files():
        if options.lightcurve:
            num, info = np.loadtxt(file, unpack=True, comments='#', usecols=(0, 6))
            
            selected.append(info[num==int(options.lightcurve)])
            
  
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(selected, 'rx')
    
    plt.show()


    
if __name__ == "__main__":
    
    parser = OptionParser(version='0.1')
    
    parser.add_option('-l', '--lc', action='store', dest='lightcurve', 
        help='extract lightcurve data')
        
    options, args = parser.parse_args()
    
    # check at least one option specified
    
    if not options.lightcurve:
        print >> sys.stderr, "Must include at least one argument"
        sys.exit(1)
    
    main(options, args)
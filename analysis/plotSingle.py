#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys

class extractSingle(object):
    """extracts single amount of data for a lightcurve
    
    'Raw' data must be in ascii table form with columns
    representing a single aperture, and rows being the 
    flux values taken per frame
    
    data must have header information with aperture numbers
    
    
    """
    def __init__(self, fileName):
        """Set up data internally"""
        super(extractSingle, self).__init__()
        self._fileName = fileName
        
        try:
            self._file = open(self._fileName)
        except IOError:
            print >> sys.stderr, "File %s not found" % self._fileName
            sys.exit(1)
        
        self._header = self._file.readlines()[0]
        self._file.close()
        
        self._aps = np.array(self._header.strip().split()[1:])
        
        try:
            self._ldata = np.loadtxt(self._fileName)
        except IOError:
            print >> sys.stderr, "File %s not found" % self._fileName
            exit(1)
        
    def singleApData(self, ap):
        """returns data for single aperture"""
        return self._ldata[:, ap]
        
    def __getitem__(self, item):
        """returns data for aperture 'item'
        
        called by extractSingle_instance[apno]
        
        """
        
        try:
            assert(item in self._aps)
        except AssertionError:
            print >> sys.stderr, "Aperture %s not found in data" % item
            return None
        else:        
            return self._ldata[:, item]
        

def main(args):
    
    usage = "Program usage: %s <file> <ap>" % args[0]

    data = extractSingle(args[1])
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

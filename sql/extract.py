#!/usr/bin/env python

import sys
import numpy as np
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import sqlite3
import matplotlib.pyplot as plt
#from IPython.Shell import IPShellEmbed


def main():
    conn = sqlite3.connect('./data.db')
    c = conn.cursor()

    c.execute('select name from sqlite_master where type="table"')
    r = c.fetchall() 
    for entry in r:
        print entry[0]



    #xcoords = []
    #ycoords = []
    #for row in c:
    #   xcoords.append(row[1])
    #   ycoords.append(row[2])

    #t = np.arange(len(xcoords)) 
    #plt.subplot(211)
    #plt.plot(t, xcoords, 'rx')
    #plt.subplot(212)
    #plt.plot(t, ycoords, 'rx')
    #plt.show()

if __name__ == '__main__':
    main()


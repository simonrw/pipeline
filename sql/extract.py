#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import sqlite3
import matplotlib.pyplot as plt
#from IPython.Shell import IPShellEmbed


def main():
    conn = sqlite3.connect('./data.db')
    c = conn.cursor()

    c.execute('select * from testtable')
    xcoords = []
    ycoords = []
    for row in c:
       xcoords.append(row[1])
       ycoords.append(row[2])

    plt.scatter(xcoords, ycoords)
    plt.show()

if __name__ == '__main__':
    main()


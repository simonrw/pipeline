#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import sqlite3
#from IPython.Shell import IPShellEmbed


def main(dir):

    try:
        conn = sqlite3.connect('./data.db')
    except:
        print >> sys.stderr, "Error connecting to database file"
        exit(1)


    dir = dir.rstrip('/')

    filelist = os.listdir(dir)
    c = conn.cursor()

    

    for file in filelist:
        fileptr = open(dir + '/' + file)
        for line in fileptr.readlines():
            if '#' not in line:
                t = line.split()[:9]
                c.execute("""insert into testtable values (?,?,?,?,?,?,?,?,?)""", t)
        fileptr.close()

    conn.commit()
    c.close()


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print >> sys.stderr, "Program usage: %s dir" % sys.argv[0]
        exit(1)
    main(sys.argv[1])


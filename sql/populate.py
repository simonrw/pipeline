#!/usr/bin/env python

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
import sqlite3
#from IPython.Shell import IPShellEmbed


def main(dir):

    conn = sqlite3.connect('./data.db')
    
    #get list of tables
    c = conn.cursor()
    c.execute('select name from sqlite_master where type="table"') #get list of tables
    r = c.fetchall()

    num = []

    for entry in r:
        num.append(entry[0].split("_")[-1])

    print num
    exit(0)


    dir = dir.rstrip('/')

    filelist = os.listdir(dir)

    

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


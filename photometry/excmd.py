#!/usr/bin/env python

from sys import argv, stderr

def main(dir):
    dir = dir.rstrip('/')
    f = open(dir + '/.cmd')
    lines = f.readlines()
    f.close()
    for line in lines:
        print line,




if __name__ == '__main__':

    if len(argv) != 2:
        print >> stderr, "Program usage: %s dir" % argv[0]
        exit(1)

    main(argv[1])


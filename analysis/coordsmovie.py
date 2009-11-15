#!/usr/bin/env python2.5

import sys
import os
import matplotlib.pyplot as plt
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
#from IPython.Shell import IPShellEmbed


def main(options, args):
    datadir = args[0].rstrip('/')
    files = os.listdir(datadir)
    files.remove('cmd')



    for i, file in enumerate(files):
        f = open(datadir + '/' + file)
        xcoords = []
        ycoords = []
        for line in f:
            if '#' not in line:
                words = line.split()
                xcoords.append(words[1])
                ycoords.append(words[2])

        f.close()
        plt.plot(xcoords, ycoords, 'ro', markersize=20, markerfacecolor='white')
        plt.title('Frame %d' % i)
        plt.axis([0, 1024, 0, 1024])
        filename = file.split('.')[0] + '.png'
        plt.savefig('/tmp/' + filename, dpi=100)
        plt.clf()

    command = ('mencoder',
               'mf:///tmp/*.png',
               '-mf',
               'type=png:w=800:h=600:fps=25',
               '-ovc',
               'lavc',
               '-lavcopts',
               'vcodec=mpeg4',
               '-oac',
               'copy',
               '-o',
               'output.avi')

    os.spawnvp(os.P_WAIT, 'mencoder', command)
    p = Popen('rm -f /tmp/*.png', shell=True, stdout=PIPE, stderr=STDOUT)
    p.communicate()

if __name__ == '__main__':

    parser = OptionParser()

    options, args = parser.parse_args()
    main(options, args)


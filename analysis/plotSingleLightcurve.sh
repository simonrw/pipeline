#!/bin/bash

file=`mktemp`

/home/astro/phrfbf/work/phd/pipeline/analysis/extractSingle.sh $@ > $file
echo "set term wx; unset key; plot '${file}' u 1" | gnuplot -persist 2> /dev/null

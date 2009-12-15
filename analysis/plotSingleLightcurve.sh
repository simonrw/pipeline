#!/bin/bash

file=`mktemp`

./extractSingle.sh $@ > $file
echo "set term wx; unset key; plot '${file}' u 1" | gnuplot -persist

#!/bin/bash
#typeset -i str

if [ "$#" != 2 ]
then
    echo "Program usage: ${0} <file> <column>"
    exit
fi

file=$1
col=$2

if [ $col == "0" ]
then
    echo "Please choose non-zero column value"
    exit
fi

header=$(cat $file | head -n 1)

aps=`echo "val = \"${header}\".strip().split(); del val[0]; print val[:]" | python | sed 's/\[//' | sed 's/\]//' | sed 's/,//g' `

let flag=0
let count=0

for ap in $aps
do
    if [ $ap = "'${col}'" ]
    then
        let flag=1
        break
    else
        let count=$((count + 1))
    fi
done

let count=$((count + 1))

if [ $flag -eq 1 ]
then

    length=$(cat $file | wc -l)
    length=$((length - 1))
    cat $file | tail -n ${length} | awk "{print \$${count}}"

else
    echo "Aperture not found"
fi


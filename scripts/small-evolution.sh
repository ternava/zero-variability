#!/bin/bash

git clone git://git.sv.gnu.org/coreutils > /dev/null 2>&1
cd coreutils

VERSIONS=$(git tag | grep v. | sort -V | tr '\n' ' ')
OUT="/tmp/small.csv"

small="arch expr factor false groups hostid hostname link logname nohup printf sleep test true tsort unlink uptime users whoami yes"


echo "version $small"
for vers in $VERSIONS
do
    git checkout -f $vers > /dev/null 2>&1
    printf "%s " $vers
    for prog in $small
    do
        loc="-"
        src="src/$prog.c"
        if [ -f $src ]; then
            loc=$(cloc --csv $src | grep C | cut -d ',' -f5)
        fi
        printf "%s " $loc
    done
    echo
done

cd ..

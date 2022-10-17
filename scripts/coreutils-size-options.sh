#!/bin/bash

# set -x

if [ ! -d "coreutils-9.1/" ] ; then
    echo "coreutils-9.1 source does not exist"
    echo "Downloading coreutils-9.1..."
    curl -O https://ftp.gnu.org/gnu/coreutils/coreutils-9.1.tar.gz
    echo "Decompressing coreutils-9.1.tar.gz..."
    tar xf coreutils-9.1.tar.gz
fi
echo "coreutils-9.1 does exist, entering directory..."
cd coreutils-9.1
pgs=$(head -n 18 README | tail -n 9 | tr ' ' '\n' | sort | uniq | sed 's/install/ginstall/g')
npgs=$(echo $pgs | tr ' ' '\n' | wc -l)
echo "There are $npgs programs."

if [ -f lib/config.h ] ; then
    echo "Already configured."
else
    echo "Configure..."
    ./configure --enable-install-program=arch,hostname >> /dev/null
fi

if [ -f src/yes ] ; then
    echo "Already built."
else
    echo "Building..."
    make -j$(nproc) >> /dev/null
fi

# Quick check
for p in $pgs
do
    f=$(grep -Rl "PROGRAM_NAME \"$p\"" src)
    if [ -f $src ]; then
        echo "$p: $f"
    else
        echo "$p: NULL"
    fi
done

# echo "program options size"

# for p in $pgs
# do
#     s=$(du -b src/$p | cut -f1)
#     f=$(./src/$p --help | grep -E "^((  )|(      ))(-|\+)((-?)([A-Za-z1-9]))" | wc -l)
#     if [ $f -eq 0 ]; then # If 0 options (e.g., "test"), consider at least
#                           # --help and --version
#         f=2
#     fi
#     printf "%s %s %s\n" "$p" "$f" "$s"
# done

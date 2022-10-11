#!/bin/bash

# set -x

git clone git@github.com:landley/toybox.git > /dev/null 2>&1
cd toybox

# without "coreutils"
coreutilstools="[ arch b2sum base32 base64 basename basenc cat chcon chgrp chmod chown
chroot cksum comm cp csplit cut date dd df dir dircolors dirname
du echo env expand expr factor false fmt fold groups head hostid hostname
id install join kill link ln logname ls md5sum mkdir mkfifo mknod mktemp
mv nice nl nohup nproc numfmt od paste pathchk pinky pr printenv printf ptx
pwd readlink realpath rm rmdir runcon seq sha1sum sha224sum sha256sum
sha384sum sha512sum shred shuf sleep sort split stat stdbuf stty sum sync
tac tail tee test timeout touch tr true truncate tsort tty uname unexpand
uniq unlink uptime users vdir wc who whoami yes"

[[ ! -d change ]] && make allyesconfig && make -j96 change > /dev/null 2>&1

echo "program loc size"

for t in $coreutilstools
do
    if [ -f change/$t ]; then
        siz=$(du -b change/$t | cut -f1)
        # experimental: extract #options from --help's output
        # opt=$(./change/$t --help | grep -E "^(-|\+)?((-?)([A-Za-z1-9]))")
        src=$(find toys/ -name "$t.c")
        if [[ $src ]]; then
            loc=$(cloc --csv $src | grep C | cut -d ',' -f5)
        else
            loc="-"
        fi
    else
        loc="-"
        siz="-"
    fi
    echo "$t $loc $siz"
done

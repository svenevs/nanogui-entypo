#!/usr/bin/env bash

# delete everything except for README.md, do_copy.py,
# generate.py, and this script (clean.sh)
find . -type f -not -name README.md   -a \
               -not -name do_copy.py  -a \
               -not -name generate.py -a \
               -not -name clean.sh       \
               -exec rm -f {} \;

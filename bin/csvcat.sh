#!/bin/sh

#
#  conactonate csv files with the same columns
#
o="+1"
for f in "$@"
do
  tail $o $f
  o="+2"
done

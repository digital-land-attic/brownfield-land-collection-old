#!/bin/sh

#
#  count values in a field
#
col="$1"

echo "field,value,count"

csvcut -c "$col" |
  tail +2 |
  sort |
  uniq -c |
  sort -rn |
  sed -e 's/^ *\([0-9]*\) *\(.*\) *$/'"$col"',\2,\1/'

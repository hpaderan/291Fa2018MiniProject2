#!/bin/bash
rm -f te.idx ye.idx re.idx

sort -u terms.txt | ./break.pl | db_load -c duplicates=1 -T -t btree te.idx
sort -u pdates.txt | ./break.pl | db_load -c duplicates=1 -T -t btree da.idx
sort -u prices.txt | ./break.pl | db_load -c duplicates=1 -T -t btree pr.idx
sort -u ads.txt | ./break.pl | db_load -c duplicates=1 -T -t hash ad.idx
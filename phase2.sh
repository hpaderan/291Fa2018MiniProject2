#!/bin/bash
rm -f te.idx ad.idx da.idx pr.idx

sort -u terms.txt > terms_sorted.txt
sort -u pdates.txt > pdates_sorted.txt
sort -u prices.txt > prices_sorted.txt
sort -u ads.txt > ads_sorted.txt

perl ./break.pl < terms_sorted.txt > terms2.txt
perl ./break.pl < pdates_sorted.txt > pdates2.txt
perl ./break.pl < prices_sorted.txt > prices2.txt
perl ./break.pl < ads_sorted.txt > ads2.txt

db_load -f terms2.txt -c duplicates=1 -T -t btree te.idx
db_load -f pdates2.txt -T -c duplicates=1 -t btree da.idx
db_load -f prices2.txt -T -c duplicates=1 -t btree pr.idx
db_load -f ads2.txt -T -c duplicates=1 -t hash ad.idx

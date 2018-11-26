#!/bin/bash
rm -f te.idx ad.idx da.idx pr.idx

sort -u terms.txt > terms_sorted.txt
sort -u pdates.txt > pdates_sorted.txt
sort -u prices.txt > prices_sorted.txt
sort -u ads.txt > ads_sorted.txt

perl ./break.pl < terms_sorted.txt > terms.txt
perl ./break.pl < pdates_sorted.txt > pdates.txt
perl ./break.pl < prices_sorted.txt > prices.txt
perl ./break.pl < ads_sorted.txt > ads.txt

db_load -f terms_sorted.txt -c duplicates=1 -T -t btree te.idx
db_load -f pdates_sorted.txt -T -c duplicates=1 -t btree da.idx
db_load -f prices_sorted.txt -T -c duplicates=1 -t btree pr.idx
db_load -f ads_sorted.txt -T -c duplicates=1 -t hash ad.idx

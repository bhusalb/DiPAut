#!/usr/bin/env sh

for file in $(ls ./k_min_max_examples/*.dipa | sort -n); do
  echo $file
  time python main.py -input $file
done

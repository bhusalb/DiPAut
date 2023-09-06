#!/usr/bin/env sh

for file in $(ls ./n_box_examples/*.dipa | sort -n); do
  time python main.py -input $file
done

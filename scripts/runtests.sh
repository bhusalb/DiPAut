#!/usr/bin/env sh

for file in $(ls ./examples/*/example*.dipa | sort -n); do
  python main.py -input $file
done

#!/usr/bin/env sh

for i in {9..20}; do
  n=$((i * 5))

  python scripts/n_box_example_generator.py -n $n > n_box_examples/$n\.dipa

done

#

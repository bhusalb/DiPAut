#!/usr/bin/env sh

for i in {3..20}; do
  n=$((i * 10))

  python scripts/k_min_max_example_generator.py -n $n >k_min_max_examples/$n\.dipa

done

for file in $(ls ./review_n_box_examples/*.dipa | sort -n); do
  echo $file
  time python3 main.py -input $file -m
  echo --------------------------------------------------------------
done
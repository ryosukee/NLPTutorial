#!/bin/sh

python -O train_nn.py -i 1000 -l 5 4 3 2 1 -f 03-train-input.txt 
python -O test_nn.py -n nn.dump -f 03-test-input.txt > result.temp
python grade-prediction.py result.temp 03-train-input.txt

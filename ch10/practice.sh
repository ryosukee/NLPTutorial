#!/bin/sh

python -O train_nn.py -i 10 -l 2 1 -f titles-en-train.labeled 
python -O test_nn.py -n nn.dump -f titles-en-test.word > result.temp
python grade-prediction.py result.temp titles-en-test.labeled

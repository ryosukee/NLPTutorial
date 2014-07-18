#!usr/bin/python
#coding:utf-8
import sys
import math
from collections import defaultdict
from test_unigram import *

lam1 = .95
lam2 = .95
N = 1000000
# エントロピー
H = .0

unigram_dict = test_unigram(sys.argv[1], sys.argv[2], lam1, N)
pml_dict = defaultdict(lambda:0)
words_count = 0

# モデルからpmlの取得
for line in open(sys.argv[1]):
	pml_dict[line.strip().split("\t")[0]] = float(line.strip().split("\t")[1])

# テストの文字からエントロピーを求める
for line in open(sys.argv[2]):
	preword = ""
	words = line.strip().split(" ")
	words.insert(0, "<s>")
	for word in words:
		if preword != "":
			H -= math.log(lam2 * pml_dict[preword+" "+word] + (1-lam2)*unigram_dict[word], 2)
			words_count += 1
		preword = word
print "entropy = %f" % (H/words_count)

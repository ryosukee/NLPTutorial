#!usr/bin/python
#coding:utf-8
import sys
import math
from collections import defaultdict

pml_dict = defaultdict(lambda:0)
# 語数
N = 1000000
# エントロピー	
H = .0
# 未知語でない確率
lam = 0.95
# 文書中に出てきた未知語の数
unk_count = .0
# 文書中に出てきた単語の数
words_count = .0

# モデルからpmlの取得
for line in open(sys.argv[1]):
	pml_dict[line.strip().split("\t")[0]] = float(line.strip().split("\t")[1])

# エントロピーを加算していく
for line in open(sys.argv[2]):
	words = line.strip().split(" ")
	words.append("</s>")
	for word in words:
		H -= math.log(lam * pml_dict[word] + (1-lam)/N, 2)
		words_count += 1
		if pml_dict[word] == 0:
			unk_count += 1

print "entropy = %f" % (H/words_count)
print "coverage = %f" % ((words_count-unk_count)/words_count)

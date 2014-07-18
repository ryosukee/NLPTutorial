# !usr/bin/python
# coding:utf-8
import sys
import math
from collections import defaultdict
from unigram import *

count = 0
words_dict = defaultdict(lambda:0)
bigram_dict = defaultdict(lambda:0)
for line in open(sys.argv[1]):
	words = line.strip().split()
	words.append("</s>")
	words.insert(0, "<s>")
	preword = ""
	for word in words:
		words_dict[word] += 1
		if preword != "":
			bigram_dict[preword+" "+word] += 1
		count += 1
		preword = word

for key, value in sorted(bigram_dict.items()):
	print "%s\t%f" % (key, float(value)/words_dict[key.split(" ")[0]])
for key, value in sorted(train_unigram(sys.argv[1]).items()):
	print "%s\t%f" % (key, value)

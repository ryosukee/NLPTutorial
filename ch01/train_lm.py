# !usr/bin/python
# coding:utf-8
import sys
import math
from collections import defaultdict

count = 0
words_dict = defaultdict(lambda:0)
for line in open(sys.argv[1]):
	words = line.strip().split(" ")
	words.append("</s>")
	for word in words:
		words_dict[word] += 1
		count += 1

for key, value in sorted(words_dict.items()):
	print "%s\t%f" % (key, float(value)/count)

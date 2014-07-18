# !usr/bin/python
# coding:utf-8
import sys
import math
from collections import defaultdict

def train_unigram(arg):
	count = 0
	words_dict = defaultdict(lambda:0)
	for line in open(arg):
		words = line.strip().split(" ")
		# words.append("</s>")
		for word in words:
			words_dict[word] += 1
			count += 1
	for key, value in sorted(words_dict.items()):
		words_dict[key] = float(value)/count
	return words_dict

#!usr/bin/python
#coding:utf-8
import sys
import math
from collections import defaultdict

"""
arg1:モデルのファイル名
arg2:テストデータ
lam:未知語でない確率
N:語数
"""
def test_unigram(arg1, arg2, lam, N):
	words_dict = defaultdict(lambda:0)
	pml_dict = defaultdict(lambda:0)
	
	# モデルからpmlの取得
	for line in open(arg1):
		pml_dict[line.strip().split("\t")[0]] = float(line.strip().split("\t")[1])

	# テストの文字と確率のMapを作る
	for line in open(arg2):
		words = line.strip().split(" ")
		#words.append("</s>")
		for word in words:
			words_dict[word] = lam * pml_dict[word] + (1-lam)/N
	return words_dict

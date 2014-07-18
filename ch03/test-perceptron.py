# !/usr/bin/python
# coding:utf-8

u"""
パーセプトロンテスト
"""

import sys
import math
from collections import defaultdict

def create_features(string):
	u"""
	文字列から素性を作成する
	@parm string 入力文字列
	@return 素性の辞書 
	"""
	features = defaultdict(lambda:0)
	for word in string.strip().split(" "):
			features["UNI:"+word] += 1
	return features

def predict(string, features, weight):
	u"""
	素性と重みからネガポジを推測する
	@parm string 推測したい入力文字列
	@parm features 素性の辞書
	@parm weight 重みの辞書
	@return -1 or 1
	"""
	score = 0
	for word in string.strip().split(" "):
		score += features["UNI:"+word]*weight["UNI:"+word]
	return 1 if score>=0 else -1

if __name__ == "__main__":
	weight = defaultdict(lambda:0)

	# 重みの読み込み
	for line in open(sys.argv[1]):
		weight[line.strip().split("\t")[0]] = int(line.strip().split("\t")[1])

	for line in open(sys.argv[2]):
		print predict(line.strip(), create_features(line.strip()), weight)

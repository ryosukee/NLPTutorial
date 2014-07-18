# !/usr/bin/python
# coding:utf-8

u"""
パーセプトロントレーニング
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

def predict(features, weight):
	u"""
	素性と重みからネガポジを推測する
	@parm features 素性の辞書
	@parm weight 重みの辞書
	@return -1 or 1
	"""
	score = 0
	for name, value in features.items():
		score += value*weight[name]
	return 1 if score>=0 else -1

def update_weight(features, weight, p_or_m):
	u"""
	重みを更新する
	@parm features 素性の辞書
	@parm weight 重みの辞書
	@parm p_or_m 1 or -1
	@return 重みの辞書
	"""
	for name, value in features.items():
		weight[name]+=value*p_or_m
	return weight


def perceptron(arg):
	u"""
	パーセプトロンのアルゴリズムで重みを学習して返す。
	@parm arg ラベル付きデータのファイル名
	@return 重みの辞書
	"""
	weight = defaultdict(lambda:0)
	for line in open(arg):
		string = line.strip().split("\t")[1]
		label = int(line.strip().split("\t")[0])
		features = create_features(string)
		if label != predict(features, weight):
			weight = update_weight(features, weight, label)
	return weight

if __name__ == "__main__":
	for uniword, weight in sorted(perceptron(sys.argv[1]).items()):
		print uniword+"\t"+str(weight)



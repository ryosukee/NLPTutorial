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
    features = defaultdict(lambda: 0)
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
    return 1 if score >= 0 else -1


def update_weight(features, weight, p_or_m, c):
    u"""
    パーセプトロンによる重みの学習
    @parm features 素性の辞書
    @parm weight 重みの辞書
    @parm p_or_m 1 or -1
    @parm c 正則化定数
    @return 重みの辞書
    """
    # 正則化
    for name, value in weight.items():
        if abs(value) <= c:
            weight[name] = 0
        else:
            weight[name] -= value/abs(value) * c

    for name, value in features.items():
        weight[name] += value*p_or_m
    return weight


def perceptron(arg, margin, c):
    u"""
    パーセプトロンのアルゴリズムで重みを学習して返す。
    @parm arg ラベル付きデータのファイル名
    @parm c 正則化係数
    @return 重みの辞書
    """
    weight = defaultdict(lambda: .0)
    for i in range(20):
        for line in open(arg):
            string = line.strip().split("\t")[1]
            label = int(line.strip().split("\t")[0])
            features = create_features(string)
            if sum(weight[name] * features[name] for name in features.keys()) * label <= margin:
                weight = update_weight(features, weight, label, c)
    return weight

if __name__ == "__main__":
    margin = .1
    c = .0001
    for uniword, weight in sorted(perceptron(sys.argv[1], margin, c).items()):
        print uniword+"\t"+str(weight)



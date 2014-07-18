#!/usr/bin/python
#coding:utf-8
import sys
import random
from math import tanh
from collections import defaultdict
from argparse import ArgumentParser
import pickle
from train_nn import *
"""
パーセプトロンをつなげてNN
コマンドライン引数に各層のパーセプトロンの数を渡す
eg, 5 4 2 1
だと層1に5個, 層2に4個,,,

NN : dict {階層0~n: パーセプトロンのリスト}

"""

def sign(num):
    return 1 if num > 0 else -1


def create_features(string):
    """
    文字列から素性を作成する
    @parm string 入力文字列
    @return 素性の辞書
    """
    features = defaultdict(lambda: 0)
    for word in string.strip().split(" "):
            features["UNI:"+word] += 1
    return features


def main():
    parser = ArgumentParser(description=
                            "{0} [Args] [Options]\n"
                            "Detailed options -h or --help".format(__file__))
    parser.add_argument(
        "-n", "--nn",
        required=True,
        dest="nn_file",
        help="学習したnnのファイル名"
    )

    parser.add_argument(
        "-f", "--file",
        required=True,
        dest="file_name",
        help="入力ファイル名"
    )

    args = parser.parse_args()

    nn = pickle.load(open(args.nn_file))

    # NNの予測をする
    for line in open(args.file_name):
        last_parceptron = None
        features_list = [create_features(line.strip())]
        # 予測
        for layer, findex in zip(nn.keys(), range(len(nn.keys()))):
            if __debug__: print "\nlayer", layer
            next_feature = dict()
            for perceptron in nn[layer]:
                perceptron.predict(features_list[findex])
                next_feature[perceptron.getID()] = perceptron.getPredict()
                last_parceptron = perceptron
            features_list.append(next_feature)
        print sign(last_parceptron.getPredict())

if __name__ == '__main__':
    main()

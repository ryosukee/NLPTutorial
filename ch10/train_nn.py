#!/usr/bin/python
#coding:utf-8
import sys
import random
from math import tanh
from collections import defaultdict
from argparse import ArgumentParser
import pickle

"""
パーセプトロンをつなげてNNを学習する
nn : dict {階層0~n: パーセプトロンのリスト}
"""


class Perceptron:
    """
    パーセプトロンを表すクラス
    クラス変数
        int _instance_num:  これまでに生成されたインスタンスの数, int
        float _lam:   学習率, float
    """
    _instance_num = int()
    _lam = .5

    def __init__(self):
        """
        @parm   _ID インスタンスのユニークなID, int
        @parm   _weight 素性の重み, dict
        @parm   _last_predict   最後に予測した時の出力値, float
        @parm   _delta  逆伝搬するときに必要な項, float
        """
        Perceptron._instance_num += 1
        self._ID = Perceptron._instance_num
        self._weight = dict()
        # self._weight = defaultdict(lambda: random.uniform(-.01, .01))
        self._last_predict = float()
        self._delta = float()

    def predict(self, features):
        """
        素性からラベルを予測する
        ついでに予測値を_last_predictに保存しておく
        初めて予測するときは、重みをランダムに(-0.01~0.01)初期化する
        @oarm   features 素性, dict
        @return 予測した値, float
        """
        if __debug__: print "-\npredict:", self._ID
        for key in features.keys():
            if not key in self._weight:
                self._weight[key] = random.uniform(-.01, .01)
        score =0
        for ID in features.keys():
            # if ID in self._weight:
            score += self._weight[ID] * features[ID]
        self._last_predict = tanh(score)

        # self._last_predict = tanh(sum(self._weight[ID] * features[ID]
        #                           for ID in features.keys() if ID in self._weight))
        if __debug__: print "predict:", self._last_predict
        return self._last_predict

    def update_delta(self, perceptron_list, true_label):
        # if __debug__: print "-\nupdate delta"
        # もしこの層が最後の層なら
        if len(perceptron_list) == 0:
            self._delta = true_label - self._last_predict
        else:
            self._delta = ((1 - self._last_predict**2) *
                           sum(p.getDelta()*p.getWeight(self._ID)
                           for p in perceptron_list))
        if __debug__: print "delta:", self._delta
        
    def update_w(self, perceptron_list, true_label, features):
        """
        デルタを更新して、重みを更新する
        @parm   perceptron_list 一つ後ろの層のパーセプトロンのリスト
        @parm   true_label  真のラベル
        """
        # if __debug__: print "update w:", self._ID

        # 重みの更新
        for key in features.keys():
            self._weight[key] += Perceptron._lam * self._delta * features[key]
            # if __debug__: print "key:", key, "+=", Perceptron._lam * self._delta * self._weight[key]

    def getWeight(self, key):
        """
        素性の任意の要素keyについての重みを返す
        keyはパーセプトロンのIDだったりunigramだったり
        """
        return self._weight[key]

    def getID(self):
        return self._ID

    def getPredict(self):
        return self._last_predict

    def getDelta(self):
        return self._delta


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
        "-i", "--iteration",
        type=int,
        dest="iteration",
        default=1,
        help="イテレーション回数"
    )
    parser.add_argument(
        "-l", "--layer",
        required=True,
        nargs="+",
        dest="layer",
        help="各層のパーセプトロンの数, 低い層から順に"
    )
    parser.add_argument(
        "-f", "--file",
        required=True,
        dest="file_name",
        help="入力ファイル名"
    )

    args = parser.parse_args()

    nn = defaultdict(list)

    # 各層にパーセプトロンを作る
    for num_of_perceptron, layer in zip(args.layer, range(len(args.layer))):
        for i in range(int(num_of_perceptron)):
            nn[layer].append(Perceptron())

    # NNの学習をする
    count = 0
    result = []
    for line in open(args.file_name):
        count += 1
        # print "line:", count
        if __debug__: print "\n----\nline:", line
        true_label = int(line.strip().split("\t")[0])
        last_parceptron = None
        # iterationを回す
        for i in range(args.iteration):
            if __debug__: print "-------iteration:", i+1, "-------"
            features_list = [create_features(line.strip().split("\t")[1])]
            # 予測
            for layer, findex in zip(nn.keys(), range(len(nn.keys()))):
                if __debug__: print "\nlayer", layer
                next_feature = dict()
                for perceptron in nn[layer]:
                    perceptron.predict(features_list[findex])
                    next_feature[perceptron.getID()] = perceptron.getPredict()
                    last_parceptron = perceptron
                features_list.append(next_feature)
            # 逆伝搬
            for layer in reversed(nn.keys()):
                for perceptron in nn[layer]:
                    perceptron.update_delta(nn[layer+1], true_label)
                    perceptron.update_w(nn[layer+1], true_label, features_list[layer])
        if __debug__:
            print "t:", true_label, "p:", sign(last_parceptron.getPredict())
            result.append((true_label, sign(last_parceptron.getPredict())))
    if __debug__:
        print "-----------"
        for r in result:
            print r[0] == r[1], "t:", r[0], "p:", r[1]

    if __debug__:
        for key , value in sorted(nn[0][0]._weight.items(), key = lambda x: x[1]):
            print key, value

    pickle.dump(dict(nn), open("nn.dump", "wb"))

if __name__ == '__main__':
    main()

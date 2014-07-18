#!/usr/bin/python
#coding:utf-8
import argparse
from collections import defaultdict
import pickle

# 定数
SHIFT = "shift"
RIGHT = "right"
LEFT = "left"
UNK = "unk"


class Token:
    def __init__(self, ID, word, surface, pos, pos1, head, label):
        self.ID = ID
        self.word = word
        self.surface = surface
        self.pos = pos
        self.pos1 = pos1
        self.head = head
        self.label = label


class Stack:
    def __init__(self, l=list()):
        self._l = l

    def push(self, item):
        self._l.append(item)

    def pop(self):
        return self._l.pop(-1)

    def pop_second(self):
        return self._l.pop(-2)

    def getFirst(self):
        return self._l[-1]

    def getSecond(self):
        try:
            return self._l[-2]
        except IndexError:
            return None

    def hasOverTwo(self):
        return len(self._l) >= 2


class Queue:
    def __init__(self):
        self._l = list()

    def enQueue(self, item):
        self._l.append(item)

    def deQueue(self):
        return self._l.pop(0)

    def isEmpty(self):
        return len(self._l) == 0

    def getIter(self):
        for item in self._l:
            yield item

    def getFirst(self):
        return self._l[0]
        

def getArgs():
    # パーサーの生成
    parser = argparse.ArgumentParser(description="ShiftReduceによる係り受け解析のテスト")
    
    # オプション引数の追加
    parser.add_argument(
        "-f", "--file",
        dest="conll_file",
        required=True,
        help="CoNLL形式の入力ファイル"
    )

    parser.add_argument(
        "-m", "--model",
        dest="model_file",
        required=True,
        help="重みのモデルファイル"
    )
    
    return parser.parse_args()


def make_features(queue, stack):
    features = dict()
    if not queue.isEmpty():
        features["W-1 "+stack.getFirst().word+" W0 "+queue.getFirst().word] = 1
        features["W-1 "+stack.getFirst().word+" P0 "+queue.getFirst().pos] = 1
        features["P-1 "+stack.getFirst().pos+" W0 "+queue.getFirst().word] = 1
        features["P-1 "+stack.getFirst().pos+" P0 "+queue.getFirst().pos] = 1
    if stack.getSecond() is not None:
        features["W-2 "+stack.getSecond().word+" W-1 "+stack.getFirst().word] = 1
        features["W-2 "+stack.getSecond().word+" P-1 "+stack.getFirst().pos] = 1
        features["P-2 "+stack.getSecond().pos+" W-1 "+stack.getFirst().word] = 1
        features["P-2 "+stack.getSecond().pos+" P-1 "+stack.getFirst().pos] = 1

    return features


def predict_action(queue, stack, features):
    score_shift = int()
    score_l_reduce = int()
    score_r_reduce = int()
    for key in features.keys():
        score_shift += weight[SHIFT][key] * features[key]
        score_l_reduce += weight[LEFT][key] * features[key]
        score_r_reduce += weight[RIGHT][key] * features[key]

    # Shiftと推測
    if not queue.isEmpty() and score_r_reduce <= score_shift and score_l_reduce <= score_shift:
        return SHIFT
    # LeftReduceと推測
    elif score_r_reduce <= score_l_reduce and stack.hasOverTwo():
        return LEFT
    # RightReduceと推測
    elif stack.hasOverTwo():
        return RIGHT
    elif not queue.isEmpty():
        return SHIFT
    else:
        return UNK



def acction(predicted, queue, stack):
    if predicted == SHIFT:
        stack.push(queue.deQueue())
    elif predicted == RIGHT:
        # 右(first)が子 左(second)が親としてつなぐ
        # 子にした右(first)をpopする
        stack.getFirst().head = stack.getSecond().ID
        stack.pop()
    else:
        # 上の逆
        stack.getSecond().head = stack.getFirst().ID
        stack.pop_second()


def predict(queue):
    stack = Stack([Token(0, "ROOT", "ROOT", "ROOT", "ROOT", -1, "None")])
    while not queue.isEmpty() or stack.hasOverTwo():
        # 素性の作成
        features = make_features(queue, stack)
        # shift-reduceの予測
        predicted = predict_action(queue, stack, features)
        # 推測だと絶対にうまく終わらないパターンもある
        if predicted == UNK:
            break
        # ワンステップ分操作
        acction(predicted, queue, stack)


def main():
    queue = Queue()
    temp_unproc = defaultdict(int)
    for line in open(args.conll_file):
        # 1文のqueueを作る
        if line.strip() != "":
            tab_split = line.strip().split("\t")
            ID = int(tab_split[0])
            word = tab_split[1]
            surface = tab_split[2]
            pos = tab_split[3]
            pos1 = tab_split[4]
            head = -2 # テストなので読み取らない
            label = tab_split[7]
            queue.enQueue(Token(ID, word, surface, pos, pos1, head, label))
        else:
            #トークンのリストを、並び順を初期状態のキューのままでとっておく。(出力のために並び順を変えないリストをとっておく)
            tok_list = list()
            for tok in queue.getIter():
                tok_list.append(tok)
            # 推測する
            predict(queue)

            # 出力
            for tok in tok_list:
                print "%d\t%s\t%s\t%s\t%s\t-\t%i\t%s" %\
                      (tok.ID, tok.word, tok.surface, tok.pos, tok.pos1, tok.head, tok.label)
            print

            # 初期化
            queue = Queue()


if __name__ == '__main__':
    # オプション引数
    args = getArgs()

    # 重み
    weight = pickle.load(open(args.model_file))

    main()


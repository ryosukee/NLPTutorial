#!/usr/bin/python
#coding:utf-8
import argparse
from collections import defaultdict
import pickle

# 定数
SHIFT = "shift"
RIGHT = "right"
LEFT = "left"


class Token:
    def __init__(self, ID, word, surface, pos, pos1, head, label, unproc=0):
        self.ID = ID
        self.word = word
        self.surface = surface
        self.pos = pos
        self.pos1 = pos1
        self.head = head
        self.label = label
        self.unproc = unproc


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
    parser = argparse.ArgumentParser(description="ShiftReduceによる係り受け解析の学習")
    
    # オプション引数の追加
    parser.add_argument(
        "-f", "--file",
        dest="conll_file",
        required=True,
        help="CoNLL形式の入力ファイル"
    )

    parser.add_argument(
        "-d", "--dump",
        dest="dump_file",
        required=True,
        help="重みのモデルをダンプするファイル"
    )

    parser.add_argument(
        "-i", "--iter",
        dest="iter_num",
        type=int,
        default=1,
        help="イテレーション回数",
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


def make_correct_action(queue, stack, features):
    if stack.getSecond() is None:
        return SHIFT
    # 右(first)が親 左(second)が子 かつ 左(second)子に子供がいない
    elif stack.getSecond().head == stack.getFirst().ID and stack.getSecond().unproc == 0:
        return LEFT
    # 左(second)が親 右(first)が子 かつ 右(first)子に子供がいない
    elif stack.getFirst().head == stack.getSecond().ID and stack.getFirst().unproc == 0:
        return RIGHT
    else:
        return SHIFT


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
    elif score_r_reduce <= score_l_reduce:
        return LEFT
    # RightReduceと推測
    else:
        return RIGHT


def update_weight(predicted, correct, features):
    if predicted != correct:
        for key in features.keys():
            # 間違えて予測した方は低く、正しかった方は高くなるように重みを調整
            weight[predicted][key] -= features[key]
            weight[correct][key] += features[key]
    

def acction(correct, queue, stack):
    if correct == SHIFT:
        stack.push(queue.deQueue())
    elif correct == RIGHT:
        # 右(first)が子 左(second)が親としてつなぐので、左(second)親のunprocを減らす
        stack.getSecond().unproc -= 1
        # 子にした右(first)をpopする
        stack.pop()
    else:
        # 上の逆
        stack.getFirst().unproc -= 1
        stack.pop_second()


def train(queue):
    stack = Stack([Token(0, "ROOT", "ROOT", "ROOT", "ROOT", -1, "None")])

    while not queue.isEmpty() or stack.hasOverTwo():
        # 素性の作成
        features = make_features(queue, stack)
        # shift-reduceの予測
        predicted = predict_action(queue, stack, features)
        # shift-reduceの正解
        correct = make_correct_action(queue, stack, features)
        # 重み更新
        update_weight(predicted, correct, features)
        # ワンステップ分操作
        acction(correct, queue, stack)


def main():
    for i in range(args.iter_num):
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
                head = int(tab_split[6])
                label = tab_split[7]
                queue.enQueue(Token(ID, word, surface, pos, pos1, head, label))
                temp_unproc[head] += 1
            else:
                # unprocを完成させる
                for tok in queue.getIter():
                    tok.unproc = temp_unproc[tok.ID]
  
                # 学習する
                train(queue)
                print
                # 初期化
                temp_unproc = defaultdict(int)
                queue = Queue()

    pickle.dump(weight, open(args.dump_file, "w"))

if __name__ == '__main__':
    # 重み
    weight = dict()
    weight[RIGHT] = defaultdict(int)
    weight[LEFT] = defaultdict(int)
    weight[SHIFT] = defaultdict(int)

    # オプション引数
    args = getArgs()

    main()


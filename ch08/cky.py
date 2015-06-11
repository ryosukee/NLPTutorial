# !/usr/bin/python
# coding:utf-8
import sys
from collections import defaultdict
import math

class Edge:
    def __init__(self, subNode1, subNode2):
        """
        @parm    subNode1    片方のノード
        @parm    subNode2    もう片方のノード
        """
        self.subNode1 = subNode1
        self.subNode2 = subNode2
class Node:
    def __init__(self, tag, logprob=None, edge=None, lnum=None, rnum=None, word=""):
        """
        @parm    tag    タグ(句), 終端の場合は文字
        @parm    logprob    ノードの対数確率
        @parm    edge    NodeがつながっているEdge
        @parm    lnum    左の添字
        @parm    rnum    右の添字
        @parm    word    葉ノードの時に対応する文字
        """
        self.tag = tag
        self.logprob = logprob
        self.edge = edge
        self.lnum = lnum
        self.rnum = rnum
        self.word = word

    def __str__(self):
        if not self.isLeaf():
            return self.tag +", "+ str(self.logprob) +", "+ str(self.lnum) +", "+ str(self.rnum)+", "+self.edge.subNode1.tag+", "+self.edge.subNode2.tag
        return self.tag +", "+ str(self.logprob) +", "+ str(self.lnum) +", "+ str(self.rnum) +", "+ self.word

    def isLeaf(self):
        """
        このノードが葉(末端)ノードかどうか
        葉ノード:文字
        @return    葉ノードであればTrue
        """
        return self.edge is None

def getPennTreebank(node):
    if not node.isLeaf():
        return "("+node.tag+" "+getPennTreebank(node.edge.subNode1)+" "+getPennTreebank(node.edge.subNode2)+")"
    else:
        return "("+node.tag+" "+node.word+")"

if __name__ == '__main__':
    grammar_file = sys.argv[1]
    input_file = sys.argv[2]

    grammar_dict = defaultdict(list)
    # 文法ファイルを読み込む
    print "get grammar_dict"
    for line in open(grammar_file):
        # P(l→r) → d[r]=(l, P)
        grammar_dict[line.rstrip().split("\t")[1]].append((line.rstrip().split("\t")[0], float(line.rstrip().split("\t")[2])))

    #入力ファイルを読み込む
    for line in open(input_file):
        print "get leaf node"
        words = line.rstrip().split()
        node_list = []
        # 前終端記号の(葉)ノードをリストに入れる
        for word, lnum in zip(words, range(0, len(words))):
            for tag, prob in grammar_dict[word]:
                node_list.append(Node(tag, -math.log(prob, 2), None, lnum, lnum+1, word))
        for node in node_list:
            print node
        
        print "get other node"
        # その他のノードをリストに入れる
        for rnum in range(2, len(words)+1): # 右の添字
            for lnum in range(0, rnum-1)[::-1]: # 左の添字
                # ノードの左の添字と別のノードの右の添字がこのループで回してる添字と一致するノード同士で総当り
                for lNode in [node for node in node_list if node.lnum == lnum]:
                    for rNode in [node for node in node_list if node.rnum == rnum and node.lnum==lNode.rnum]:
                        print lnum, rnum, len([node for node in node_list if node.lnum == lnum]), len([node for node in node_list if node.rnum == rnum and node.lnum==lNode.rnum])
                        if lNode.tag+" "+rNode.tag in grammar_dict:
                            for tag, prob in grammar_dict[lNode.tag+" "+rNode.tag]:
                                new_prob = -math.log(prob) + rNode.logprob + lNode.logprob
                                if [node for node in node_list if node.lnum == lnum and node.rnum == rnum and node.tag == tag]:
                                    if new_prob > [node for node in node_list if node.lnum == lnum and node.rnum == rnum][0].logprob:
                                        node_list.append(Node(tag, new_prob, Edge(lNode, rNode), lnum, rnum))
                                else:
                                    node_list.append(Node(tag, new_prob, Edge(lNode, rNode), lnum, rnum))
        for node in node_list:
            print node

        # 出力
        # ノードリストの中から、タグがSで かつ 左の添字が0で かつ 右の添字が文字数 であるノードのリストを取得し、
        # それを対数確率の降順でソートした、最初の要素がルートノード
        print len([node for node in node_list if node.tag == "S" and node.lnum==0 and node.rnum==len(words)])
        root_node = sorted([node for node in node_list if node.tag == "S" and node.lnum==0 and node.rnum==len(words)], key = lambda x: -x.logprob)[0]
        print "print tree"
        # 後はルートノードをたどる
        print getPennTreebank(root_node)

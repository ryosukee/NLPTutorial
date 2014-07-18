# !usr/bin/python
# coding:utf-8
import sys
import math
from collections import defaultdict

class Node:
	def __init__(self, best_edge, best_score):
		self.best_edge = best_edge
		self.best_score = best_score
	def __str__(self):
		if self.best_edge is not None:
			return self.best_edge.word.encode("utf-8")+", "+str(self.best_score)
		else:
			return "None, "+str(self.best_score)

class Edge:
	def __init__(self, word, from_node, score):
		self.word = word
		self.from_node = from_node
		self.score = score

def front_step(prob_dict, input_filename):
	for line in open(input_filename):
		nodeList = []
		nodeList.append(Node(None, 0))

		line = unicode(line, "utf-8")
		# エッジの終端を決める
		for word_end in range(1, len(line)):
			# エッジの始点を決める
			for word_start in range(0, word_end):
				word = line[word_start:word_end].strip()
				#もし未知語であり、かつ長さが1以上なら
				if not word in prob_dict and len(word)!=1:
					continue
				# unigramの確率とエッジの始点ノードのスコアを足したもの
				score = nodeList[word_start].best_score - math.log(prob_dict[word],2)
				# print "debug:", word.encode("utf-8"), score
				# 既にエッジの終点ノードが作ってあり、かつ、そのノードのスコアよりも計算したスコアが小さければ、ノードを更新
				if len(nodeList)>word_end and score < nodeList[word_end].best_score:
					nodeList[word_end].best_score = score
					nodeList[word_end].best_edge = Edge(word, nodeList[word_start], -math.log(prob_dict[word],2))
				# まだエッジの終点ノードが作られていなければ、ノードを追加
				elif len(nodeList)<=word_end:
					nodeList.append(Node(Edge(word, nodeList[word_start], -math.log(prob_dict[word],2)), score))
				# どちらでもない場合(もうあるけど、既にあるスコアの方が小さい)なにもしない
				else:
					pass
		# for node in nodeList:
		# 	print node
		# ひと通り前向きステップが終わったら、できたノードリストで後ろ向きステップを行う
		back_step(nodeList)

def back_step(nodeList):
	currentNode = nodeList[-1]
	path = [currentNode]
	# 再帰的にノードのベストエッジをたどる
	while(currentNode.best_edge is not None):
		path.append(currentNode.best_edge.from_node)
		currentNode = currentNode.best_edge.from_node
	# 出力
	path.reverse()
	for node in path:
		if node.best_edge is not None:
			print node.best_edge.word.encode("utf-8"),
	print""


if __name__ == '__main__':
	# 未知語の確率
	ram = .1**10
	probmodel_filename = sys.argv[1]
	prob_dict = defaultdict(lambda:ram)
	# unigramの確率の辞書を作る
	for line in open(probmodel_filename):
		prob_dict[unicode(line.strip().split("\t")[0], "utf-8")] = float(line.strip().split("\t")[1])
	front_step(prob_dict, sys.argv[2])


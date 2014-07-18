# !usr/bin/python
# coding:utf-8
import sys
import math
from collections import defaultdict

class Node:
	def __init__(self, word="", tag="", best_score=100000000, best_pre_node=None):
		self.word = word
		self.tag = tag
		self.best_score = best_score
		self.best_pre_node = best_pre_node
	def __str__(self):
		return "id:"+str(id(self))+",word:"+self.word+",tag:"+self.tag+",score:"+str(self.best_score)+",prenode:"+str(id(self.best_pre_node))

# 前向きステップ
def front_step(tag_list, trans_dict, emit_dict, inputfile):
	for line in open(inputfile):
		words = line.strip().split()
		words.append("</s>")
		# ノードリストはタグをキーとした辞書で定義
		node_list = defaultdict(Node)
		pre_node_list = defaultdict(Node)
		pre_node_list["<s>"] = Node("", "<s>", 0, None)
		for word in words:
			# 前のノードと現在のノードの組み合わせで回す
			for pre_node in pre_node_list.values():
				# もし終端記号だったらタグごとに回す必要はない
				if word is "</s>" and pre_node.tag+" </s>" in trans_dict:
					new_score = pre_node.best_score - math.log(trans_dict[pre_node.tag+" </s>"], 2)
					node_list["</s>"] = Node(word, "</s>", new_score, pre_node) if node_list["</s>"].best_score > new_score else node_list[tag]
				for tag in tag_list:
					# 遷移確率の辞書に存在する遷移しか確かめない(遷移確率は平滑化しない)
					if pre_node.tag+" "+tag in trans_dict:
						new_score = pre_node.best_score - math.log(trans_dict[pre_node.tag+" "+tag], 2) - math.log(emit_dict[tag+" "+word], 2)
						node_list[tag] = Node(word, tag, new_score, pre_node) if node_list[tag].best_score > new_score else node_list[tag]
			pre_node_list = node_list.copy()
			node_list.clear()
		back_step(pre_node_list["</s>"])

# 後ろ向きステップ
def back_step(node):
	tags = []
	node = node.best_pre_node
	while node.best_pre_node is not None:
		tags.append(node.tag)
		node = node.best_pre_node
	tags.reverse()
	print " ".join(tags)


if __name__ == '__main__':
	modelfile = sys.argv[1]
	inputfile = sys.argv[2]

	tag_list = set()
	trans_dict = {}
	emit_dict = defaultdict(lambda:.000000001)

	#モデル読み込み
	for line in open(modelfile):
		words = line.strip().split()
		if words[0] is "T":
			trans_dict[words[1]+" "+words[2]] = float(words[3])
		else:
			emit_dict[words[1]+" "+words[2]] = float(words[3])
			tag_list.add(words[1])

	# 前向きステップ
	front_step(tag_list, trans_dict, emit_dict, inputfile)

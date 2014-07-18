# !usr/bin/python
# coding:utf-8
__author__ = "ryosuke"
__date__ = "2014/06/1"

import sys
import math
from collections import defaultdict

class Node:
	"""
	"""
	def __init__(self, kana="", conversion="", best_score=100000000, best_pre_node=None):
		self.kana = kana
		self.conversion = conversion
		self.best_score = best_score
		self.best_pre_node = best_pre_node
	def __str__(self):
		return "id:"+str(id(self))+",kana:"+self.kana.encode("utf-8")+",conversion:"+self.conversion.encode("utf-8")+",score:"+str(self.best_score)+",prenode:"+str(id(self.best_pre_node))

# 前向きステップ
def front_step(trans_dict, emit_dict, inputfile, ram1, ram2, N):
	if __debug__: print "front_step"
	for line in open(inputfile):
		line = unicode(line.strip(), "utf-8")
		# ノードリストは、word_endを添え字としたリストで、中身は漢字をキーとしたノードのdict
		# ノードリストの初期化　これをnode_list = [defaultdict(Node)]*(len(line)+2)で一括でやろうとすると
		# リストの全ての要素が同じdefaultdictになっちゃうから、一つ一つインスタンス化する
		node_list = [0]*(len(line)+2)
		for i in range(0, len(node_list)):
			node_list[i] = defaultdict(Node)
		node_list[0]["<s>"] = Node("", "<s>", 0, None)
		node_list[-1]["</s>"] = Node("", "</s>", 10000000, None)

		# かなの終端を決める
		for word_end in range(1, len(line)+2):
			# かなの始点を決める
			for word_start in range(0, word_end):
				kana = line[word_start:word_end].strip()
				if __debug__: print "\n",kana.encode("utf-8"), "kana"
				# word_startの位置にあるノードと現在のノードの組み合わせで回す
				for pre_node in node_list[word_start].values():
					if __debug__: print "pre_node", pre_node

					# もし終端記号だったら生成確率は計算しない
					if kana == "":
						if __debug__: print "---</s>---"
						# 平滑化のための計算
						unigram = ram1 * trans_dict["</s>"] + (1-ram1)/N
						bigram = ram2 * trans_dict[pre_node.conversion+" </s>"] + (1-ram2)*unigram
						# スコア計算
						new_score = pre_node.best_score - math.log(bigram, 2)
						node_list[word_end]["</s>"] = Node(kana, "</s>", new_score, pre_node) if node_list[word_end]["</s>"].best_score > new_score else node_list[word_end]["</s>"]
						if __debug__: print "更新後:", node_list[word_end]["</s>"]
					else:
						# 生成確率の辞書に存在するもので計算する
						con_pro_list=[]
						if kana not in emit_dict and len(kana)==1:
							con_pro_list = [(kana, .1**10)]
						elif kana in emit_dict:
							con_pro_list = emit_dict[kana]
						for conversion, em_prov in con_pro_list:
							if __debug__: print conversion.encode("utf-8"), "conv"
							# 平滑化のための計算
							unigram = ram1 * trans_dict[conversion] + (1-ram1)/N
							bigram = ram2 * trans_dict[pre_node.conversion+" "+conversion] + (1-ram2)*unigram
							# スコア計算
							new_score = pre_node.best_score - math.log(bigram, 2) - math.log(em_prov, 2)
							node_list[word_end][conversion] = Node(kana, conversion, new_score, pre_node) if node_list[word_end][conversion].best_score > new_score else node_list[word_end][conversion]
							if __debug__: print "更新後:", node_list[word_end][conversion]
		if __debug__: 
			for ddd in node_list:
				for nnn in ddd.values():
					print nnn
		back_step(node_list[-1]["</s>"].best_pre_node)

# 後ろ向きステップ
def back_step(node):
	if __debug__: print "back_step"
	conversions = []
	while node.best_pre_node is not None:
		conversions.append(node.conversion)
		node = node.best_pre_node
	conversions.reverse()
	print " ".join(conversions).encode("utf-8")


if __name__ == '__main__':
	em_modelfile = sys.argv[1]
	tr_modelfile = sys.argv[2]
	inputfile = sys.argv[3]

	ram1 = .95
	ram2 = .95
	N = 1000000

	emit_dict = defaultdict(list)
	trans_dict = defaultdict(float)
	prov_dict = {}

	#モデル読み込み
	# emit_dict : かなをキーとした変換後,確率のタプル
	# trans_dict : 変換後をキーとした確率
	for line in open(em_modelfile):
		words = line.strip().split()
		emit_dict[words[1].decode("utf-8")].append((words[0].decode("utf-8"), float(words[2])))
	for line in open(tr_modelfile):
		words = line.strip().split("\t")
		trans_dict[words[0].decode("utf-8")] = float(words[1])
	nondefault_emitd = {}
	nondefault_emitd.update(emit_dict)

	# 前向きステップ
	front_step(trans_dict, nondefault_emitd, inputfile, ram1, ram2, N)


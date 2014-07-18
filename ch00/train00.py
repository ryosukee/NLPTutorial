#!/usr/bin/python
#coding:utf-8
import sys
#keyに単語、valueに出現回数を入れる辞書my_dictを作る
from collections import defaultdict
my_dict = defaultdict(lambda:0)

#ファイルから１行読み込み、空白で分割した単語のvalueを+1する、なければ登録もしてくれる
for line in open(sys.argv[1], "r"):
	for word in line.strip().split(" "):
		my_dict[word]+=1

#できた辞書を回して出力
for word, value in sorted(my_dict.items()):
	print word +", "+str(value)


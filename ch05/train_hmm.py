# !usr/bin/python
# coding:utf-8
import sys
from collections import defaultdict

trans_dict = defaultdict(lambda:.0)
emit_dict = defaultdict(lambda:.0)
tag_dict = defaultdict(lambda:.0)
start_word = "<s>_<s>"
end_word = "</s>_</s>"

# ここでカウント
for line in open(sys.argv[1]):
	words = line.strip().split()
	words.insert(0, start_word)
	words.append(end_word)
	pre_tag = ""
	for word in words:
		word_tag = word.split("_")
		# タグのユニグラムカウント
		tag_dict[word_tag[1]] += 1
		# タグと文字(生成)のバイグラムカウント
		if word is not start_word and word is not end_word:
			emit_dict[word_tag[1]+" "+word_tag[0]] += 1
		# タグのバイグラムカウント
		if pre_tag is not "":
			trans_dict[pre_tag+" "+word_tag[1]] +=1
		pre_tag = word_tag[1]

# ここで計算、出力
for key, value in sorted(trans_dict.items()):
	print "T", key, value/tag_dict[key.split()[0]]
for key, value in sorted(emit_dict.items()):
	print "E", key, value/tag_dict[key.split()[0]]

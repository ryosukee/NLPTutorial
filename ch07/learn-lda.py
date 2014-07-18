# /usr/bin/python
# coding:utf-8

from collections import defaultdict
import sys
import random
import math

NUM_TOPICS=10
ALPHA = .001
BETA = .001
Nw = 0
Nt = NUM_TOPICS

words_corpus=[]
topics_corpus=[]
words_count = defaultdict(int)
topics_count = defaultdict(int)

def AddCount(word, topic, docid, amount):
	words_count[str(topic)] += amount
	words_count[word+"|"+str(topic)] += amount
	topics_count[str(docid)] += amount
	topics_count[str(topic)+"|"+str(docid)] += amount

def SampleOne(probs):
	remaining = random.uniform(0, sum(probs))
	for i in range(0, len(probs)):
		remaining -= probs[i]
		if remaining <= 0:
			# if __debug__: print "sampling:", i
			return i

if __name__ == '__main__':
	# 初期化
	for line in open(sys.argv[1]):
		docid = len(words_corpus)
		topics = []
		words = line.strip().split()
		for word in words:
			topic = random.randint(0, NUM_TOPICS-1)
			topics.append(topic)
			AddCount(word, topic, docid, 1)
			Nw += 1
		words_corpus.append(words)
		topics_corpus.append(topics)

	# if __debug__:
	# 	print "wcount:", words_count
	# 	print "tcount:", topics_count

	# サンプリング
	ll=0
	for loop_num in range(0, 1000):
		for docid in range(0, len(words_corpus)):
			for wordid in range(0, len(words_corpus[docid])):
				word = words_corpus[docid][wordid]
				topic = topics_corpus[docid][wordid]
				# if __debug__: print "word:", word, "\n", "topic:", topic, "\ndocid:", docid
				AddCount(word, topic, docid, -1)
				probs=[]
				for topic in range(0, NUM_TOPICS):
					# if __debug__: print "pxy, top:", float(words_count[word+"|"+str(topic)]+ALPHA)
					# if __debug__: print "pxy, bottom:", (words_count[str(topic)]+ALPHA)
					# if __debug__: print "pyy, top:", float(topics_count[str(topic)+"|"+str(docid)]+BETA)
					# if __debug__: print "pyy, bottom:", topics_count[str(docid)]+BETA
					# if __debug__: print words_corpus, "\n", topics_corpus

					prob = (float(words_count[word+"|"+str(topic)]+ALPHA) / (words_count[str(topic)]+ALPHA)) * (float(topics_count[str(topic)+"|"+str(docid)]+BETA) / (topics_count[str(docid)]+BETA) )
					probs.append(prob)
				# if __debug__: print "probs:", probs
				new_topic = SampleOne(probs)
				ll -= math.log(probs[new_topic])
				AddCount(word, new_topic, docid, 1)
				topics_corpus[docid][wordid] = new_topic
				if __debug__: print loop_num, "周, 対数尤度:", ll, "\n\n"
	#出力
	result_dict=defaultdict(list)
	for docid in range(0, len(words_corpus)):
		for wordid in range(0, len(words_corpus[docid])):
			result_dict[topics_corpus[docid][wordid]].append(words_corpus[docid][wordid])
	for topic, words in result_dict.items():
		print topic, ": ",
		for word in sorted(set(words)):
			print word,
		print ""
	# for docid in range(0, len(words_corpus)):
	# 	for wordid in range(0, len(words_corpus[docid])):
	# 		print words_corpus[docid][wordid], topics_corpus[docid][wordid]

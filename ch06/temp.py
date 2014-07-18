#!usr/bin/python
#coding:utf-8
import sys

for line in open(sys.argv[1]):
	line = unicode(line.strip(), "utf-8")
	print line[0]

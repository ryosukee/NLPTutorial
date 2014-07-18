#coding:utf-8
import sys

d={}
for line in open(sys.argv[1]):
    for tok in line.strip().split():
        d[tok] = 0

print len(d.keys())

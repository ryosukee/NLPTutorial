#coding:utf-8
import pickle

weight = pickle.load(open("weight.dump"))

for key, value in sorted(weight.items()):
    print key, value

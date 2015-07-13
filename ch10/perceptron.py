# coding:utf-8

import random
import math

class Perceptron:
    def __init__(self, name, lam):
        self._weight = dict()
        self._name = name
        self._delta = 0
        self._predict = 0
        self._lam = lam

    def predict(self, inputs):
        score = 0
        for name in inputs.keys():
            # init weight
            if not name in self._weight:
                self._weight[name] = random.uniform(-.01, .01)
            score += inputs[name] * self._weight[name]
        self._predict = math.tanh(score)

    def calc_delta(self, next_perceptrons, label=None):
        if label:
            self._delta = label - self._predict
        else:
            s = sum(p.get_delta() * p.get_weight(self._name) for p in next_perceptrons)
            self._delta = (1 - self._predict ** 2) * s

    def update_weight(self, inputs):
        for name in inputs.keys():
            self._weight[name] += self._lam * self._delta * inputs[name]
    
    def get_delta(self):
        return self._delta

    def get_weight(self, name):
        return self._weight[name]

    def get_predict(self):
        return self._predict

    def get_name(self):
        return self._name

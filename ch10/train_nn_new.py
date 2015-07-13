# coding:utf-8
"""

Usage:
    train_nn_new.py [--lam <lam>] [--output <outfile>] -l <n>... --train <train> [--epoch <epoch>]

Options:
    --lam <lam>
        learning late [default: .5]
    --output <outfile>
        output file [default: nn_model.pkl]
    -l
        the opsion of hiden layers and hiden units
    --train <train>
        train file
    --epoch <epoch>
        epoch num [default: 100]
"""

import pickle
from docopt import docopt
from perceptron import Perceptron

__author__ = 'ryosuke'
__version__ = '0.0.0'
__data__ = 20150709

def init():
    layers = list()
    count = 0
    for i in args['<n>']:
        parceptrons = list()
        for j in range(i):
            parceptrons.append(Perceptron(count, args['--lam']))
            count += 1
        layers.append(parceptrons)
    return layers


def front_propergation(layers, inputss):
    for layer in layers:
        inputs = dict()
        for perceptron in layer:
            perceptron.predict(inputss[-1])
            inputs[perceptron.get_name()] = perceptron.get_predict()
        inputss.append(inputs)
    inputss.pop(-1)

def back_propergation(layers, inputss, gold):
    prev_layer = None
    for layer, inputs in zip(layers[::-1], inputss[::-1]):
        for perceptron in layer:
            if prev_layer is None:
                perceptron.calc_delta(None, label=gold)
            else:
                perceptron.calc_delta(prev_layer)
            perceptron.update_weight(inputs)
        prev_layer = layer

def train(layers):
    inputss = list()
    for line in open(args['--train']):
        spl = line.strip().split()
        gold = spl[0]

        # create feature
        feats = dict()
        for feat in spl[1:]:
            feats[feat] = feats.get(feat, 0) + 1 
        inputss.append(feats)
        
        front_propergation(layers, inputss)
        back_propergation(layers, inputss, float(gold))


def main():
    layers = init()
    for _ in range(args['--epoch']):
        train(layers)
    pickle.dump(layers, open(args['--output'], 'w')) 

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    args['<n>'] = [int(i) for i in args['<n>'] if i.isdigit()]
    args['--lam'] = float(args['--lam'])
    args['--epoch'] = int(args['--epoch'])
    main()

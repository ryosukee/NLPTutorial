# coding:utf-8
"""

Usage:
    train_nn_new.py [--output <outfile>] --test <test> --model <model>

Options:
    --output <outfile>
        output file [default: result.txt]
    --test <test>
        test file
    --model <model>
        trained nn model
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
    return inputss.pop(-1).values()[0]



def test(layers):
    inputss = list()
    with open(args['--output'], 'w') as fw:
        for line in open(args['--test']):
            words = line.strip().split()
    
            # create feature
            feats = dict()
            for feat in words:
                feats[feat] = feats.get(feat, 0) + 1 
            inputss.append(feats)
            
            output = front_propergation(layers, inputss)
            print >> fw, '-1' if output < 0 else '1'


def main():
    layers = pickle.load(open(args['--model']))
    test(layers)

if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    main()

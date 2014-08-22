#!usr/bin/python
#coding:utf-8
import sys
import math
import argparse
"""
test the unigram language model
"""

__author__ = "marujirou"
__version__ = "1.0"
__date__ = "2014/08/22"


def getArgs():
    """
    optional argument setting
    """
    parser = argparse.ArgumentParser(description="test the language model")

    parser.add_argument(
        "-f", "--input",
        dest="test_file",
        type=argparse.FileType("r"),
        required=True,
        help="input filename as test data"
    )

    parser.add_argument(
        "-l", "--lm",
        dest="lm_file",
        type=argparse.FileType("r"),
        required=True,
        help="language model file"
    )

    parser.add_argument(
        "-o", "--output",
        dest="eval_file",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output filename as evaluation result"
    )

    return parser.parse_args()


def get_pml():
    """
    get Pml from language model
    @return Pml dict
    """
    pml = dict()
    for line in args.lm_file:
        word = line.strip().split("\t")[0]
        prob = float(line.strip().split("\t")[1])
        pml[word] = prob

    return pml


def calc_eval(pml, lam, N):
    """
    calculate words probability used interpolation, and calculate evaluations
    @parm pml probability of unigram dict
    @parm lam interpolation coefficient of unigram
    @parm N type of words include unknown words
    @return (entropy, perplexity, coverage)
    """
    words_count = .0
    unk_count = .0
    H = .0
    p = dict()
    for line in args.test_file:
        words = line.strip().split()
        words.append("</s>")
        for word in words:
            p[word] = lam * pml.get(word, 0) + (1-lam)/N
            H -= math.log(p[word], 2)
            if word not in pml:
                unk_count += 1
            words_count += 1

    H = H/words_count
    coverage = (words_count-unk_count)/words_count
    perplexity = 2**H

    return H, perplexity, coverage


def main():
    # type of words include unknown words
    N = 10**6
    # interpolation coefficient of unigram
    lam_one = 0.95

    # get pml
    pml = get_pml()
    # calculate evaluations
    H, perplexity, coverage = calc_eval(pml, lam_one, N)

    print >> args.eval_file, "entropy : %f" % H
    print >> args.eval_file, "perplexity : %f" % perplexity
    print >> args.eval_file, "coverage : %f" % coverage


if __name__ == '__main__':
    args = getArgs()
    main()

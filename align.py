#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import fileinput
import random
import sys

#######################################################

def lexicalPT(filename):

    condprob = defaultdict(lambda: defaultdict(int))

    for line in fileinput.input(filename):
        value, given, prob = line.strip().split()
        condprob[value][given] = float(prob)

    return condprob

#######################################################

def align(source, target, lexPT):
    print("Aligning {} and {}".format(source,target))
    result=[]

    for j in range(0, len(target)):

        # Calculate conditional probability of source word i given target word j, for all values of i
        probs = [ lexPT[source[i]][target[j]] for i in range(0, len(source)) ]

        # Get the maximum
        bestProb = max(probs)

        # Get all values of i that have that maximum probability
        bestIndices = [i for i, prob in enumerate(probs) if prob == bestProb]

        # Calculate the absolute distance between j and each possible i
        distances = [abs(j-i) for i in bestIndices]

        # Get the smallest of the distances
        minDistance = min(distances)

        # Get all indices i which both have bestProb and minDistance
        bestIndicesWithMinDistance = [bestIndices[k] for k, distance in enumerate(distances) if distance==minDistance]

        # If there are more than one value of i with max prob and minDistance
        #    randomly select one of them
        i = random.choice(bestIndicesWithMinDistance)

        result.append("{}-{}".format(i,j))

    return result


#######################################################


if __name__ == '__main__':
    
    if len(sys.argv) < 1:
        print("Usage: {} lexPT".format(sys.argv[0]), file=sys.stderr)
        exit(-1)

    else:

        lexPT = lexicalPT(sys.argv[1])
        
        for line in sys.stdin:

            source, target, _ = line.strip().split(" ||| ")

            alignments = align(source.split(), target.split(), lexPT)

            print(" ".join(alignments))



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
import fileinput
import random
import re
import sys
import xmlrpc.client

#######################################################
# Globals

groupSeparator="Moses::ContextScope::GroupSeparator"

recordSeparator="Moses::ContextScope::RecordSeparator"

dynamicPTName="DynamicPT0"
dynamicLMName="DynamicLM0"

#######################################################

def lexicalPT(filename):

    condprob = defaultdict(lambda: defaultdict(int))

    for line in fileinput.input(filename):
        value, given, prob = line.strip().split()
        condprob[value][given] = float(prob)

    return condprob

#######################################################

def align(source, target, lexPT):
#    print("Aligning \"{}\" (length {}) and \"{}\" (length {})".format(source,len(source),target,len(target)))
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

#    print(" ".join(result))
    return result


#######################################################

def phraseTable(topts, sourceWords, indexedSourceWords, featureName, lexPT):

    result=""

    for topt in topts:
        start=topt["start"]
        end=topt["end"]+1
        indexed_source_phrase=" ".join(indexedSourceWords[start:end])
        source_phrase=" ".join(sourceWords[start:end])
        target_phrase=topt["phrase"]
        alignment = " ".join(align(source_phrase.split(), target_phrase.split(), lexPT))
        scores=topt["labelledScores"][featureName][0]
        result += "{} ||| {} ||| {} ||| {}\n".format(indexed_source_phrase, target_phrase, " ".join([str(score) for score in scores]), alignment)
        
    return result
        
#######################################################


def static_moses(port, text):
    url = "http://localhost:{}/RPC2".format(port)
    proxy = xmlrpc.client.ServerProxy(url)
    params = {
        "text":text,
        "topt":"true",
        "word-align":"true",
        "align":"true",
        "no-ReportSegmentation":"true"
    }
    return proxy.translate(params)


#######################################################


def dynamic_moses(port, text, contextScope):

    url = "http://localhost:{}/RPC2".format(port)

    proxy = xmlrpc.client.ServerProxy(url)
    params = {
        "text":text,
        "topt":"true",
        "context-scope":contextScope,
    }
    return proxy.translate(params)


#######################################################

def indexSourceWords(sourceSentence):

    result = []
    words = sourceSentence.split()

    for source_index in range(0,len(words)):
        result.append(words[source_index] + "@" + str(source_index))
    
    return result


#######################################################


def ppe(staticPort, dynamicPort, lexPT, inputs):

    for sourceSentence in fileinput.input(inputs):

        sourceSentence = sourceSentence.strip()
        indexedSourceWords = indexSourceWords(sourceSentence)

        staticResult = static_moses(staticPort, sourceSentence)
        if 'align' in staticResult:
            print(staticResult['align'])
            print()
        if 'word-align' in staticResult:
            print(staticResult['word-align'])
            print()
        
        print(staticResult['topt'])
        print()

        staticTranslation = re.sub(r"UNK\S+", "<unk>", staticResult['text']).strip()
        print("Source:\t{}\nTarget:\t{}".format(sourceSentence, staticTranslation))
        print()

        completePT = phraseTable(staticResult['topt'], sourceSentence.split(), indexedSourceWords, "StaticPT0", lexPT)

        print(completePT)
        print()

        contextScope = "DynamicPT0" + recordSeparator + completePT

        dynamicResult = dynamic_moses(dynamicPort, " ".join(indexedSourceWords), contextScope) 
        dynamicTranslation = re.sub(r"UNK\S+", "<unk>", dynamicResult['text'].strip())

        print("Target:\t{}".format(dynamicTranslation))



#######################################################


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("Usage: {} staticPort dynamicPort lexPT [sourceText]".format(sys.argv[0]), file=sys.stderr)
        exit(-1)

    else:

        ppe(sys.argv[1], sys.argv[2], lexicalPT(sys.argv[3]), sys.argv[4:]+["-"])


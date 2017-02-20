#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import fileinput
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

def phraseTable(topts, source, featureName):

    result=""

    for topt in topts:
        start=topt["start"]
        end=topt["end"]+1
#        print(start + ":" + end)
#        source_phrase = source[start] + "@0" 
#        for source_index in range(start+1,end):
#            source_phrase += " " + source[source_index] + "@" + str(source_index)
        source_phrase=" ".join(source[start:end])
        target_phrase=topt["phrase"]
        scores=topt["labelledScores"][featureName][0]
        result += "{} ||| {} ||| {}\n".format(source_phrase, target_phrase, " ".join([str(score) for score in scores]))
        
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


def ppe(staticPort, dynamicPort, inputs):

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

        completePT = phraseTable(staticResult['topt'], indexedSourceWords, "StaticPT0")

        print(completePT)
        print()

        contextScope = "DynamicPT0" + recordSeparator + completePT

        dynamicResult = dynamic_moses(dynamicPort, " ".join(indexedSourceWords), contextScope) 
        dynamicTranslation = re.sub(r"UNK\S+", "<unk>", dynamicResult['text'].strip())

        print("Target:\t{}".format(dynamicTranslation))



#######################################################


if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print("Usage: {} staticPort dynamicPort [sourceText]".format(sys.argv[0]), file=sys.stderr)
        exit(-1)

    else:

        ppe(sys.argv[1], sys.argv[2], sys.argv[3:]+["-"])


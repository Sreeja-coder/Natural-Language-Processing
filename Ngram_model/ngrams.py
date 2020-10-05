import sys
import getopt
import math
import re
import collections
import random

fo = open(sys.argv[1], 'r')
f1 = open(sys.argv[3], 'r')
listofwords = []
w = fo.read()
w = w.lower()
w1 = f1.read()
temp = ''
temp2 = ''
listoftestsentences = []
noOfsentences = 0
#creating test text list
for sent in w1.split("\n"):
    listoftestsentences = w1.split("\n")

#print(listoftestsentences)
#creating listofwords from training
for word in w.split(" "):
        listofwords = w.split(" ")

#print(len(listofwords))
#creating unigram dictionary
UnigramDict = {}
for i in listofwords:
    UnigramDict[i] = listofwords.count(i)
#print(UnigramDict)

#creating bigram dictionary
bigrams = zip(*[listofwords[i:] for i in range(2)])
bigrams =(list([" ".join(ngram) for ngram in bigrams]))
bigramslist=list(bigrams)
BigramDict = {}
for i in bigramslist:
    BigramDict[i] = bigramslist.count(i)
#print(BigramDict)

#no of sentences in training set
for w2 in w.split("\n"):
    noOfsentences = noOfsentences + 1
#print(noOfsentences)


def calunigram(TestLine):
    probOfSentence =1
    #print("inside function : ",TestLine)
    for w3 in TestLine.split(" "):
        for k, v in UnigramDict.items():
            if w3.lower() == k.lower():
                p1 = v/len(listofwords)
                probOfSentence = p1*probOfSentence
    final = round(math.log(2, probOfSentence), 4)
    return final

#For Bigrams

#for case with phi
def probofwordasphi(w8):
    count = 0

    for w6 in w.split("\n"):
        for w7 in w6.split(" "):
            if w7.lower() == w8.lower():
                count = count+1
                #print("count:", count)
            break;
    return count

def calbigramprob (TestLine):
        p1 = 0
        p2 = 1
        p3 = 0
        p4 = 1

        listoftestwords = []
        listoftestwords = TestLine.split(" ")
        w4 = listoftestwords[0]
        Tbigrams = zip(*[listoftestwords[i:] for i in range(2)])
        Tbigrams = (list([" ".join(ngram) for ngram in Tbigrams]))
        #print("Tbigrams :", Tbigrams)
        #print("lenght of Tbigrams", len(Tbigrams))
        for j in range(0, len(Tbigrams)):
            if j == 0:
                #print(w4)
                p1 = probofwordasphi(w4)/noOfsentences
                p3 = probofwordasphi(w4)+1/noOfsentences
                #print("p1 value :", p1)
            if j == 1:
                nume = 1
                denom = 1
                for t in Tbigrams:
                    for k, v in BigramDict.items():
                        if t.lower() == k.lower():
                            #print("num", v)
                            nume = v
                            curr1 = k.split(" ")
                            for u, v1 in UnigramDict.items():
                                if u == curr1[0]:
                                    #print("denom" ,denom)
                                    denom =v1
                    p2 = p2*(nume/denom)
                    #print("value of p2", p2)
                    p4 = p4*(nume+1)/((denom+1)+len(BigramDict))

                    #print("value of p4", p4)
        return p2*p1, p3*p4

#For Seed sentence gen


def sentencegen(seed, counter):
    seedDict = {}
    curr4 = ''
    #print("entered in the funct")
    #print(BigramDict)
    if (seed == "." or seed == '!' or seed == ',' or counter == 5):
        return " "
    else:
        counter = counter + 1
        for k2, v2 in UnigramDict.items():
            curr3 = k2
            if seed == curr3:
                freqseed = v2
        for k1, v1 in BigramDict.items():
            curr2 = k1.split(" ")
            #print(curr2[0])
            if seed.lower() == curr2[0].lower():
                seedDict[k1] = v1/freqseed
                #print("entered the if 2")

        x = (random.randint(0, 10)/10)
        for k2, v2 in seedDict.items():
            #print("entered for")
            if x > v2 or x< v2:
                #print("entered if")
                curr4 = k2.split(" ")
                #print(curr4)
                #print(curr4[1])
                #print(type(curr4))
                temp = curr4[1]
                temp2 = curr4[0]
                #print(type(sentencegen(temp)))
            break
    return (temp2 +" "+ sentencegen(temp,counter))


for t in listoftestsentences:
    print("S=", t)
    c = calunigram(t)
    a, b = calbigramprob(t)

    if c <= 1:
        print("unsmoothed unigram prob for sentence ", "is",  round(c, 4))
    else:
        print("unsmoothed unigram prob for sentence ", "is", round(math.log(2, c)), 4)

    if a < 1:
        print("unsmoothed bigram prob for sentence ", "is", round(a, 4))

    else:
       print("unsmoothed bigram prob for sentence ", "is", round(math.log(2, a), 4))
    if b < 1:
        print("smoothed bigram prob for sentence ", "is",round(b, 4))
    else:
        print("smoothed bigram prob for sentence ", "is" , round(math.log(2, b), 4))
    print("sentence gen with seed word")
    print(sentencegen('cat', 0))
    print("      ")
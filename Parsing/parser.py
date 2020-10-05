import sys
import getopt
import math
import re
import collections
import random

def parsesentence():
    file1 = open(sys.argv[2], 'r')
    #print(file1.read())
    wordlist = {}
    operatorlist = []
    sentence = file1.read()
    count = 0
    stack = []
    finaldparse = []
    sentenceslist = []

    #print(sentence)
    for i, word in enumerate(sentence.split()):
        if word != "OPERATORS" and word != "SENTENCE:":
            wordlist[i] = word
        if word == "OPERATORS":
            count = i
            break
    #print(sentence.split("\n"))
    #for sentence1 in enumerate(sentence.split("\n")):
        sentenceslist.append(sentence.splitlines())
        #sentenceslist.append(sentence1)
    print(*sentenceslist[0], sep=', ')

    for i, word in enumerate(sentence.split()):
       ## if word == "OPERATORS":
            #operatorlist[word] = word
        if i > count:
            operatorlist.append(word)

    counter =1
    stackcounter =-1
    #print(operatorlist)
    #print(len(wordlist))
    for j in operatorlist:
        if counter <= len(wordlist)+1:
            if j == "Shift":
                print("Shifting word ", wordlist.get(counter), "(", counter, ")","onto stack")
                stack.append(wordlist.get(counter))
                stackcounter = stackcounter + 1
                counter = counter + 1
            else:
                wordtemp = j.split("_")
                #print("wordtemp [1]", wordtemp[1])
                #print("the stack",stack)
                #print(stack[stackcounter-1])
                if wordtemp[0] == "RightArc" and stackcounter > 0:
                    print("Applying",j,"to produce relation:",stack[stackcounter-1], "(", (list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter-1])]), ")","-----",wordtemp[1],"---->-",stack[stackcounter],  "(", (list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter])]), ")")
                    tempsentence = stack[stackcounter-1], (list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter-1])]), "-----",wordtemp[1],"---->-",stack[stackcounter],   (list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter])])
                    stack.pop(stackcounter)
                    stackcounter = stackcounter - 1
                    finaldparse.append(tempsentence)
                if wordtemp[0] == "LeftArc" and stackcounter > 0:
                    print("Applying", j, "to produce relation:", stack[stackcounter], "(",(list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter])]), ")","-----", wordtemp[1], "----->", stack[stackcounter-1], "(", (list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter-1])]), ")")
                    tempsentence = stack[stackcounter], ((list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter])])) ,"-----" ,wordtemp[1] , "----->" , stack[stackcounter-1] , ((list(wordlist.keys())[list(wordlist.values()).index(stack[stackcounter-1])]) )
                    stack.pop(stackcounter - 1)
                    stackcounter = stackcounter - 1
                    finaldparse.append(tempsentence)
                if stackcounter == 0 and j == "RightArc_root":
                    print("Applying",j,"to produce relation:","ROOT 0","-----",wordtemp[1],"----->",stack[stackcounter])
                    tempsentence = "ROOT 0","-----",wordtemp[1],"----->",stack[stackcounter]
                    finaldparse.append(tempsentence)

    print("Final Dependency parse :")
    for v in finaldparse:
        print(*v, sep=', ')
    #print(finaldparse)


def generateops():
    file1 = open(sys.argv[3], 'r')
    sentence = file1.read()
    wordlist = []
    sentence1 = []
    stack = []
    operators = []
    golddependency = []
    relationdict = {}
    indexdict = {}
    reversedict = {}
    count = 0
    stackcounter = -1
    for word in (sentence.split()):
        wordlist.append(word)

    #building the sentence
    for i in range(len(wordlist)):
        if wordlist[i].isdigit():
           count = count + 1
        if count == 2:
            sentence1.append(wordlist[i-1])
            count = 0

    #building the dictionary
    for word in sentence1:
        count = 0
        key = word
        relationdict.setdefault(key, [])
        for word2 in wordlist:
            if word == word2:
                index = wordlist.index(word2)
                relationdict[word].append(wordlist[index+1])
                relationdict[word].append(wordlist[index + 2])
                break
    #building index dictionary
    indexval = 1
    for word in sentence1:
        indexdict[indexval] = word
        reversedict[word] = indexval
        indexval = indexval + 1
    #print("relationdict",relationdict)
    #print("indexdict",indexdict)
    #print("reverse dict",reversedict)

    for word in sentence1:
        count = count + 1
        #print("word",word)
        stack.append(word)
        stackcounter = stackcounter + 1
        operators.append("Shift")
        #check for word dependency
        if len(stack) > 1:
            templist = []
            for w in reversed(stack):
                templist.append(w)
            counter = 0
            #print("templist",templist)
            for s in templist:
                #print("s",s)
                canremove = 0  #is true at start
                counter = counter + 1
                for word2 in relationdict:
                    if int(relationdict[word2][0]) == int(reversedict[s]):
                        canremove = 1   #there is dependecy you can't remove
                #print("for",s,"canremove",canremove)
                indexval = templist.index(s)
                if canremove == 0 and counter == 1 and int(relationdict[s][0]) == int(reversedict[templist[(indexval+1)]]):
                    temp1 = templist[indexval+1]+" "+str(reversedict[templist[indexval+1]])+"-----"+relationdict[s][1]+"--->"+templist[indexval]+" "+str(reversedict[templist[indexval]])
                    temp = "Generating RightArc _"+ relationdict[s][1]+" to produce relation:"+templist[indexval+1]+" "+str(reversedict[templist[indexval+1]])+"-----"+relationdict[s][1]+"--->"+templist[indexval]+" "+str(reversedict[templist[indexval]])
                    operators.append(temp)
                    golddependency.append(temp1)
                    relationdict[s]=[0]
                    stack.pop(stack.index(s))
                    templist[indexval] = templist[indexval+1]
                    stackcounter = stackcounter-1

                if canremove == 0 and counter != 1 and int(relationdict[s][0])== int(reversedict[templist[indexval-1]]):
                    temp1 = templist[indexval-1]+" "+str(reversedict[templist[indexval-1]])+"-----"+relationdict[s][1]+"--->"+templist[indexval]+" "+str(reversedict[templist[indexval]])
                    temp="Generating LeftArc _" + relationdict[s][1]+" to produce relation:"+templist[indexval-1]+" "+str(reversedict[templist[indexval-1]])+"-----"+relationdict[s][1]+"--->"+templist[indexval]+" "+str(reversedict[templist[indexval]])
                    operators.append(temp)
                    relationdict[s]=[0]
                    stack.pop(stack.index(s))
                    golddependency.append(temp1)
                    templist[indexval] = templist[indexval-1]

    wordindex = 0
    while len(stack) !=1:
        if len(stack) > 1:
            templist = []
            for w in reversed(stack):
                templist.append(w)
            counter = 0
            #print("templist",templist)
            for s in templist:
                #print("s",s)
                canremove = 0  #is true at start
                counter = counter + 1
                for word2 in relationdict:
                    if int(relationdict[word2][0]) == int(reversedict[s]):
                        canremove = 1   #there is dependecy you can't remove
                #print("for",s,"canremove",canremove)
                indexval = templist.index(s)
                if canremove == 0 and counter == 1 and int(relationdict[s][0]) == int(reversedict[templist[(indexval+1)]]):
                    temp1 = templist[indexval+1]+" "+str(reversedict[templist[indexval+1]])+"-----"+relationdict[s][1]+"--->"+templist[0]+" "+str(reversedict[templist[indexval]])
                    temp = "Generating RightArc _" + relationdict[s][1]+" to produce relation:"+templist[indexval+1]+" "+str(reversedict[templist[indexval+1]])+"-----"+relationdict[s][1]+"--->"+templist[0]+" "+str(reversedict[templist[indexval]])
                    operators.append(temp)
                    golddependency.append(temp1)
                    relationdict[s]=[0]
                    stack.pop(stack.index(s))
                    templist[indexval] = templist[indexval+1]
                    stackcounter = stackcounter-1

                if canremove == 0 and counter != 1 and int(relationdict[s][0])== int(reversedict[templist[indexval-1]]):
                    temp1 = templist[indexval-1]+" "+str(reversedict[templist[indexval-1]])+"-----"+relationdict[s][1]+"--->"+templist[indexval]+" "+str(reversedict[templist[indexval+1]])
                    temp="Generating LeftArc _" + relationdict[s][1]+" to produce relation:"+templist[indexval-1]+" "+str(reversedict[templist[indexval-1]])+"-----"+relationdict[s][1]+"--->"+templist[indexval]+" "+str(reversedict[templist[indexval+1]])
                    operators.append(temp)
                    golddependency.append(temp1)
                    relationdict[s]=[0]
                    stack.pop(stack.index(s))
                    templist[indexval] = templist[indexval-1]


    #print(len(stack))
    if len(stack) == 1:
        temp1="ROOT(0)"+ "----"+"root"+"--->"+stack[0]
        temp = "Generating RightArc _root to produce relation: ROOT(0)"+ "----"+"root"+"--->"+stack[0]
        operators.append(temp)
        golddependency.append(temp1)

    print("SENTENCE :",*sentence1, sep=' ')

    print("GOLD DEPENDENCIES")
    for v in golddependency:
        print(v)
    #print(operators)
    print("Final Dependency parse :")
    for v in operators:
        print(v)



argument1 = sys.argv[1]

if argument1 == "-simulate":
    parsesentence()  #call the function here
else:
    generateops()





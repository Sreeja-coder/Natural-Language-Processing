import re
import nltk
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
import sys
import os
import copy
import argparse
from collections import defaultdict


#####EXTRACTING ALL THE COREFS
def coref(inputfile,output_file,response_dir):
    #creating the output response file
    path = os.path.join(response_dir, output_filename + ".response")
    output_file = open(path, "w+")
    coref = []
    count = 0
    sentences = []
    nextline = []
    corefsent = {}
    corefiddict = {}
    sentencesdict = {}
    match = {}
    match2 = {}
    sentcoref = {}
    sentnumber = None
    sentenceidDict = defaultdict()
    with open(inputfile, "r") as input:
        lines = input.readlines()
        # print(lines)

        for element in lines:
            element.strip()
        #corefrences in list format and corefsent is a dict with coref and its line num
        for word in lines:
            count + 1
            #print("word",word)
            coref.append(re.findall(r'<COREF ID="(\w+)">([^<]+)<\/COREF>', word))
            if "COREF" in word:
                x = (re.findall(r'<COREF ID="\w+">([^<]+)<\/COREF>', word))
                y = (re.findall(r'<S ID="(\w+)">', word))
                for element in x:
                    corefsent[element] = int(y[0])
            nextline.append(re.findall(r'<S ID="\w+">([^\b]+)', word))
        nextline = [item for sublist in nextline for item in sublist]
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

        #creating list with clean sentences:
        cleansent = []
        for item in nextline:
            cleantext = re.sub(cleanr, '', item)
            # print(type(item))
            cleansent.append(cleantext)
        # print(len(cleansent))
        for element in coref:
            coref.remove([])

        corefids = [item for sublist in coref for item in sublist]
        sentenceid = [item for sublist in sentences for item in sublist] #not sure of this

        #dictionary with sentence no and sentence
        for i in range(len(cleansent)):
            sentencesdict[i] = cleansent[i]
        #dictionary of sentence num and corefid
        for element in corefids:
            corefiddict[element[0]] = element[1]

        #creating match and match2
        #match  has corefid as key and  list(POS tagged sent and line num)as value
        #match2 has corefid as key and list (sentence and line num) as value
        for val in corefiddict:
            count = 0
            for element in sentencesdict:
                match.setdefault(str(corefiddict[val]), [])
                match2.setdefault(corefiddict[val], [])
                if corefiddict[val].lower() in sentencesdict[element].lower():
                    count = count + 1
                    if count == 1:
                        sentcoref[corefiddict[val]] = element
                    x = []
                    y = nltk.pos_tag(nltk.word_tokenize(sentencesdict[element]))
                    y.append(element)
                    x.append(sentencesdict[element])
                    x.append(element)
                    match[corefiddict[val]].append(y)
                    match2[corefiddict[val]].append(x)

    #creating a dictionary with coreif as the key and the sentence num as the value
    coreference = {}
    for k, v in corefiddict.items():
        coreference[v] = k

    def matchcoref1(k,element):
        for listy in element:
            # print(listy)
            x = None
            if (len(listy) == 2):
                if (corefsent[k] == listy[len(listy) - 1]):
                    continue
                else:
                    if (listy[0][0] == ''):
                        continue
                    else:
                        output_file.write("{" + str(listy[1]) + "}" + "{" + listy[0][0] + "}")
                        output_file.write('\n')

    def matchcoref2(k,element):
        sentnumber = None
        for i in range(len(match2[k])):
            if k in match2[k][i][0]:
                if (corefsent[k] == match2[k][i][1]):
                    sentnumber = match2[k][i][1]
                    continue
                else:
                    output_file.write("{" + str(match2[k][i][1]) + "}" + "{" + k + "}")
                    output_file.write('\n')
        return sentnumber

    def synonyms(k,element,sentnumber):
        # print()
        sing_syn = []
        # sing_syn_dict={}
        for syn in wordnet.synsets(temp_list[len(temp_list) - 1].lower()):
            for l in syn.lemmas():
                # print(items,l.name())
                sing_syn.append(l.name())

        sing_syn = list(set(sing_syn))
        sing_syn_temp = []
        sing_syn.append(temp_list[len(temp_list) - 1])

        #####CLEANING MY SING_SYN_tEMP SYNONYM LIST ACCORDING TO THE HEAD NOUN (ACC TO ITS POS TAG)
        for val in sing_syn:
            sing_syn_temp.append(nltk.pos_tag(nltk.word_tokenize(val)))
        sing_syn_temp = [item for sublist in sing_syn_temp for item in sublist]
        head_tag = sing_syn_temp[-1][1]
        head_noun = sing_syn_temp[-1][0]
        # print(head_tag)
        for val in sing_syn_temp:

            # print(val)
            if (val[1] != head_tag):
                sing_syn_temp.remove(val)

        # print(sing_syn_temp)
        ##we remove the pos tags from the list
        sing_syn = []
        for element in sing_syn_temp:
            sing_syn.append(element[0])
        for s in range(sentnumber, len(sentencesdict)):
            for val in sing_syn:
                if (val == head_noun and corefsent[k] == s):
                    continue
                else:
                    if val in sentencesdict[s].split():
                        output_file.write("{" + str(s) + "}" + "{" + val + "}")
                        output_file.write('\n')

    count = 0
    for k, element in match.items():
        output_file.write("\n")
        output_file.write("<COREF ID=" + '"' + coreference[k] + '"' + ">" + k + "</COREF>")
        output_file.write('\n')
        count += 1
        temp_list = k.split()
        #we call functions according to the coref id, if they are multi words then call diff set of functions
        if len(temp_list) == 1:
            matchcoref1(k, element)
        else:
            sentnumber = matchcoref2(k, element)
            synonyms(k, element,sentnumber)

    if count == len(match):
        output_file.close()











    #reading the input args
inputfile = sys.argv[1]
responsedir = sys.argv[2]

with open(inputfile, "r") as input:
    files=input.readlines()
    #print(files)
for element in files:
    inputfile = element.strip('\n')
    #print(responsedir)
    output_files=inputfile.split('/')
    output_filename=output_files[-1]
    output_filename=re.search('(.+?).input',output_filename).group(1)
    coref(inputfile,output_filename,responsedir)
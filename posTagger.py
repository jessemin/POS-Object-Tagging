"""
This class is a class for part of speech(pos) tagging
and contains PosTagger class and can be tested with
posTaggerTest.py.
"""
import nltk
from fileUtil import *
from collections import defaultdict
import datetime
import heapq
import os
import csv
import operator


class PosTagger:
    """
    PosTagger contains a method that can parse different
    types of file, do pos tagging, and return top k prepositions.
    """
    def __init__(self, fileName="", isCsv=False, col="", k=0):
        """
        Initialize the PosTagger class.
        """
        self.prepDict = defaultdict(int)
        self.datetime = datetime.datetime.now()
        self.fileName = fileName
        self.isCsv = isCsv
        self.col = col
        self.k = k

    def run(self):
        """
        Run the main functionalities for the class.
        Do the pos tagging and returns the top k prepositions.

        :param nothing
        :return entire preposition dictionary and list of top k prepositions
        """
        self.processMultipleSentences(self.prepDict, readData(self.fileName, self.isCsv, self.col))
        return self.prepDict, self.getTopKPreps(self.k)

    def getTopKPreps(self, k):
        """
        Get top k prepositions.

        :param k
        :return list of top k prepositions
        """
        return heapq.nlargest(k, self.prepDict, key=self.prepDict.get)

    def tagSingleSentence(self, sentence):
        """
        Do pos tagging on a single sentence.

        :param sentence
        :return result of pos tagging (list of tuples)
        """
        return nltk.pos_tag(nltk.word_tokenize(sentence))

    def getPrepFromSingleSentence(self, prepDict, sentence):
        """
        Get prepositions from a single sentence.
        Directly update to the entire preposition dictionary.

        :param entire preposition dictionary
        :param sentence
        :return nothing
        """
        tags = self.tagSingleSentence(sentence)
        for (word, tag) in tags:
            if tag == "IN":
                self.prepDict[word] += 1

    def processMultipleSentences(self, prepDict, sentences):
        """
        Process multiple sentence at once.

        :param entire preposition dictionary
        :param sentences
        :return nothing
        """
        for sentence in sentences:
            self.getPrepFromSingleSentence(prepDict, sentence)

    def __str__(self):
        return 'Tagger created at: {}\nPrepositions: {}'.format(self.datetime, self.prepDict)

totalDict = {}
dataFiles = ['./data/'+filename for filename in os.listdir('./data') if filename.startswith("2016")]
for dataFile in dataFiles:
    print "Processing {}...".format(dataFile)
    tempDict, _ = PosTagger(dataFile).run()
    for key, val in tempDict.iteritems():
        if key.lower() in totalDict:
            totalDict[key.lower()] += val
        else:
            totalDict[key.lower()] = val
print "\nEntire Prepositions"
print totalDict
sorted_x = sorted(totalDict.items(), key=operator.itemgetter(1))
print sorted_x
print "\n===================================================="
print "\nTop 10 Prepositions"
print heapq.nlargest(10, totalDict, key=totalDict.get)

arrayofdata = []
for key, val in totalDict.iteritems():
    arrayofdata.append([key, key, val])

with open('./bubble/data/psych204.csv', 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    thedatawriter.writerow(["name","word","count"])
    for row in arrayofdata:
        thedatawriter.writerow(row)

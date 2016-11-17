"""
This class is a class for retrieving object, preposition
pairs and contains ObjectParser class.
"""
import jsonrpclib
from simplejson import loads

class ObjectParser:


    def __init__(self, port=8080):
        self.port = port
        self.COLOR = ["red", "blue", "green", "black", "white", "gold", "gray"]

    def setServer(self, port):
        self.server = jsonrpclib.Server("http://localhost:{}".format(str(port)))

    def parseSingleSentence(self, sentence):
        result = loads(self.server.parse(sentence))
        return result

    def getPrepositionsFromSingleSentence(self, sentence):
        prepositions = []
        parsedResult = str(self.parseSingleSentence(sentence)["sentences"][0]["parsetree"])
        index = 0
        while True:
            posInfoIdx = parsedResult.find("PartOfSpeech=IN", index)
            if posInfoIdx != -1:
                offsetBeginIdx = parsedResult.rfind("CharacterOffsetBegin=", 0, posInfoIdx) + len("CharacterOffsetBegin=")
                offsetEndIdx = parsedResult.rfind("CharacterOffsetEnd=", 0, posInfoIdx)
                offsetBegin = int(parsedResult[offsetBeginIdx:offsetEndIdx])
                offsetEndIdx += len("CharacterOffsetEnd=")
                offsetEnd = int(parsedResult[offsetEndIdx:posInfoIdx])
                prepositions.append(sentence[offsetBegin:offsetEnd])
                index = posInfoIdx + len("PartOfSpeech=IN")
            else:
                break
        return prepositions

    def getDependencies(self, sentence):
        dependencies = self.parseSingleSentence(sentence)["sentences"][0]["dependencies"]
        result = []
        for dependency in dependencies:
            nmodIdx = str(dependency[0]).find("nmod")
            if str(dependency[0]) == "nsubj":
                subject = dependency[2]
                obj = ""
                preposition = ""
                for dependency2 in dependencies:
                    if str(dependency2[0]) == "case":
                        obj = str(dependency2[1])
                        preposition = str(dependency2[2])
                        break
                result.append({"preposition": preposition, "subject": str(subject), "object": str(obj)})
            if nmodIdx != -1:
                preposition = str(dependency[0][nmodIdx+len("nmod:"):])
                result.append({"preposition": preposition, "subject": str(dependency[1]), "object": str(dependency[2])})
        return result

    def getColorObjectTuples(self, sentence):
        dependencies = self.parseSingleSentence(sentence)["sentences"][0]["dependencies"]
        result = []
        for dependency in dependencies:
            if str(dependency[0]) == "compound" or str(dependency[0]) == "amod":
                if str(dependency[2]).lower() in self.COLOR:
                    result.append({"color": str(dependency[2]), "subject": str(dependency[1])})
        return result

o = ObjectParser()
o.setServer(8080)

sampleSentence1 = "Lily is near the fountain next the mall in the red plaza."
sampleSentence2 = "A gold lily grew in the red quarter."

#sample case 1
a = o.parseSingleSentence(sampleSentence1)
print "Sample Sentence1: " + sampleSentence1
print " ----------Prepositions----------"
print o.getPrepositionsFromSingleSentence(sampleSentence1)
print " ----------Colors----------"
print o.getColorObjectTuples(sampleSentence1)
print " ----------Dependencies----------"
for b in o.getDependencies(sampleSentence1):
    print b

print "\n====================\n"

#sample case 2
a = o.parseSingleSentence(sampleSentence2)
print "Sample Sentence2: " + sampleSentence2
print " ----------Prepositions----------"
print o.getPrepositionsFromSingleSentence(sampleSentence2)
print " ----------Colors----------"
print o.getColorObjectTuples(sampleSentence2)
print " ----------Dependencies----------"
for b in o.getDependencies(sampleSentence2):
    print b

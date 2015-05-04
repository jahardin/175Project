import random
import re
import cPickle
import nltk
import time


class GenMarkov():
    def __init__(self):
        self.Timer = Timer()
        self.words = []
        self.twoGrams = {} # key = (word1, word2) & value = [possible following words]
        self.pos2G = {}
        self.sortWords = []
        self.topWords = []
        self.wordCount = {}
        self.numReviews = 500

        #self.Timer.start()
        #with open('TwoGramMarkov.pickle', 'r') as f:
        #    self.twoGrams = cPickle.load(f)
        #self.Timer.stop("Pickle Load")

        with open('pos_tagger.pickle', 'r') as f:
            self.pos_tagger = cPickle.load(f)

        # Generates two Grams from txt files
        #self.Timer.start()
        self.GatherWords()
        #self.Timer.stop("Gather Words")

        #print "WORDS GATHERED!"

        #self.Timer.start()
        self.TwoGramGen()
        #self.Timer.stop("TwoGram Generation")

        #print "TWO GRAM GENERATED!"

        #self.Timer.start()
        print self.GenRandom()
        #self.Timer.stop("Random Reivew Geneartion")

        with open('TwoGramMarkov.pickle', 'w') as f:
            cPickle.dump(self.twoGrams, f)

        #print "Two Grams Size: " + str(len(self.twoGrams))
        #print "Sort Words Size: " + str(len(self.sortWords))
        #print "Top Words Size: " + str(len(self.topWords))

    def GatherWords(self):
        start = "unsup/"
        end = "_0.txt"
        setWords = set()
        for i in xrange(self.numReviews):
            print i
            self.TokenizedWords(start+str(i)+end)

    def TokenizedWords(self,file):
        with open(file, 'r') as f:
            s = f.read()
            s = re.sub("<[^>]*>", '', s)
            try:
                words = self.pos_tagger.tag(nltk.word_tokenize(s))
            except UnicodeDecodeError:
                return
            self.words += words

    def TwoGramGen(self):
        for i in xrange(len(self.words)-2):
            if self.words[i][0] == '' or self.words[i+1][0] == '' or self.words[i+2][0] == '':
                continue
            key = (tuple(self.words[i]), tuple(self.words[i+1]))
            posKey = (self.words[i][1], self.words[i+1][1])
            val = tuple(self.words[i+2])
            posVal = self.words[i+2][1]
            keyVals = self.twoGrams.get(key)
            posKeyVals = self.pos2G.get(posKey)

            if keyVals is not None and val in keyVals:
                self.twoGrams[key][val] += 1.0
            else:
                if keyVals is None:
                    self.twoGrams[key] = {val: 1.0}
                else:
                    self.twoGrams[key][val] = 1.0

            if posKeyVals is not None and posVal in posKeyVals:
                self.pos2G[posKey][posVal] += 1.0
            else:
                if posKeyVals is None:
                    self.pos2G[posKey] = {posVal: 1.0}
                else:
                    self.pos2G[posKey][posVal] = 1.0

            for c in self.pos2G.iterkeys():
                tot = sum(self.pos2G[c].itervalues())
                for v in self.pos2G[c].iterkeys():
                    if tot != 0:
                        self.pos2G[c][v] = self.pos2G[c][v]/tot

            for c in self.twoGrams.iterkeys():
                tot = sum(self.twoGrams[c].itervalues())
                for v in self.twoGrams[c].iterkeys():
                    if tot != 0:
                        self.twoGrams[c][v] = (self.twoGrams[c][v]/tot)*self.pos2G[(c[0][1], c[1][1])][v[1]]



    def GenRandom(self, length=30):
        seed = self.GetNewSeed()

        ran = [seed[0][0], seed[1][0]]
        for i in xrange(length):
            tmp = seed[1]
            if (seed[0], seed[1]) not in self.twoGrams:
                seed = self.GetNewSeed()
            seed[1] = self.weighted_choice(self.twoGrams[(seed[0], seed[1])])
            seed[0] = tmp
            ran.append(seed[1][0])
        return " ".join(ran)

    def GetNewSeed(self):
        seedElem = random.choice(self.twoGrams.keys())
        w1 = seedElem[0]
        w2 = seedElem[1]
        seed = [w1, w2]
        return seed

    def weighted_choice(self, choices):
        total = sum(w for w in choices.itervalues())
        r = random.uniform(0, total)
        upto = 0
        for c in choices.iterkeys():
            if upto + choices[c] > r:
                return c
            upto += choices[c]
        assert False, "Shouldn't get here"


class Timer:
    def __init(self):
        self.startTime = 0
        self.endTime = 0
    def start(self):
        self.startTime = time.clock()
    def stop(self, purpose):
        self.endTime = time.clock()
        print purpose + ": " + str(self.endTime-self.startTime)

if __name__ == '__main__':
    GenMarkov()
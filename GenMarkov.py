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
        self.sortWords = []
        self.topWords = []
        self.wordCount = {}
        self.sentEnd = ['.', '!', '?']

        #self.Timer.start()
        with open('TwoGramMarkov.pickle', 'r') as f:
            self.twoGrams = cPickle.load(f)
        #self.Timer.stop("Pickle Load")


        # Generates two Grams from txt files
        #self.Timer.start()
        #self.GatherWords()
        #self.Timer.stop("Gather Words")

        #self.Timer.start()
        #self.TwoGramGen()
        #self.Timer.stop("TwoGram Generation")


        #self.Timer.start()
        #print self.GenRandom()
        #self.Timer.stop("Random Reivew Geneartion")

        #with open('TwoGramMarkov.pickle', 'w') as f:
        #    cPickle.dump(self.twoGrams, f)

        #print "Two Grams Size: " + str(len(self.twoGrams))
        #print "Sort Words Size: " + str(len(self.sortWords))
        #print "Top Words Size: " + str(len(self.topWords))

    def GatherWords(self):
        start = "unsup/"
        end = "_0.txt"
        setWords = set()
        for i in xrange(50000):
            self.TokenizedWords(start+str(i)+end)
        for x in self.words:
            if x not in setWords:
                setWords.add(x)
                self.wordCount[x] = 1
            else:
                self.wordCount[x] += 1
        with open('logRegVocab.txt') as f:
            vocab = f.read().decode('utf-8').lower()
            self.vocab = vocab.split('\r\n')
        self.sortWords = sorted(list(setWords), key=lambda w: self.wordCount[w], reverse=True)
        self.topWords = [self.sortWords[i] for i in xrange(5000)]
        self.topWordsList = list(self.topWords)
        self.topWords = set(self.topWords)
        self.fullWords = list(self.words)
        self.words = ['' if ((x not in self.topWords) and (x not in self.vocab)) else x for x in self.words]

    def TokenizedWords(self,file):
        with open(file, 'r') as f:
            s = f.read()
            s = s.lower()
            s = re.sub('<[^<]+?>', '', s)
            s = s.decode('utf-8').lower()
            s = nltk.word_tokenize(s)
            removePunc = re.compile('[\(\'"`\):;]')
            s = [w for w in s if not removePunc.search(w)]
            self.words += s


    def TwoGramGen(self):
        for i in xrange(len(self.words)-2):
            if self.words[i] == '' or self.words[i+1] == '' or self.words[i+2] == '':
                continue
            key = (self.words[i], self.words[i+1])
            val = self.words[i+2]
            keyVals = self.twoGrams.get(key)
            if keyVals is not None and val in keyVals:
                self.twoGrams[key][val] += 1
            else:
                if keyVals is None:
                    self.twoGrams[key] = {val: 1}
                else:
                    self.twoGrams[key][val] = 1

    def GenRandom(self, seed = None, length=3):
        if seed == None:
            seed = self.GetNewSeed()
        if seed[0] == '.':
            ran = [seed[1]]
        else:
            ran = [seed[0], seed[1]]
        i = 0
        w = 1
        while i < length:
            tmp = seed[1]
            if (seed[0], seed[1]) not in self.twoGrams:
                seed = self.GetNewSeed()
            seed[1] = self.weighted_choice(self.twoGrams[(seed[0], seed[1])])
            seed[0] = tmp
            ran.append(seed[1])
            w += 1
            if seed[1] in self.sentEnd:
                i += 1
                w = 0
            if w > 20:
                i += 1
                w = 0
                ran.append('.')
        return " ".join(ran)

    def GetNewSeed(self):
        seedElem = random.choice(self.twoGrams.keys())
        w1 = seedElem[0]
        w2 = seedElem[1]
        seed = [w1, w2]
        while w1 not in self.sentEnd:
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

    def findMostLikely(self, w1, w2):
        seed = [w1.lower(), w2.lower()]
        ran = [seed[0], seed[1]]
        i = 0
        while i < 1:
            tmp = seed[1]
            if(seed[0],seed[1]) not in self.twoGrams:
                break
            seed[1] = max(self.twoGrams[(seed[0], seed[1])].items(), key=lambda i: i[1])[0]
            seed[0] = tmp
            ran.append(seed[1])
            if seed[1] in self.sentEnd:
                i += 1
        return " ".join(ran)

    def GenSeed(self, seedTxt):
        thisSeed = nltk.word_tokenize(seedTxt.decode('utf-8').lower())
        return self.GenRandom(seed=thisSeed)

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
    g = GenMarkov()
    print g.GenRandom()

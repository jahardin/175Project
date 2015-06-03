import os
import nltk
import numpy
import interface



class Regression():
    test = 1111111111111111
	
    def calc_log_regression(self, wordList):
        print "Reading training set..."
            
        # get svm vocab words	
        f = open('logRegVocab.txt', 'r')
        word_features = f.read().splitlines()
        f.close()

        f2 = open('logRegScale.txt', 'r')
        word_scale = [float(i) for i in f2.read().splitlines()]
        f2.close()

        fw = open('logRegWeights.txt', 'r')
        weights = [float(i) for i in fw.read().splitlines()]
        fw.close()
        
        return self.logReg(word_features, word_scale, weights, wordList)

    def bow_features(self, word_features, word_scale, weights, document):
        words = nltk.word_tokenize(document)
        print len(words)
        features = [0] * len(word_features)
        features[0] = 1	
        for word in words:
            if word in word_features:
                features[word_features.index(word)+1] += 1
        for i in range(len(features)):
            features[i] *= word_scale[i]/(len(words))

        return features

    def logReg(self, word_features, word_scale, weights, document):
        bow = self.bow_features(word_features, word_scale, weights, document)
        z = 0
        for i in range(0,len(bow)):
            z = z + bow[i] * weights[i]
        retVal = 1 + 9 / (1 + numpy.exp(-z))
        print retVal
        return retVal
        #self.scorebox2.delete(1.0, END)
        #self.scorebox2.insert(INSERT, retVal)
        #return 1 + 9 / (1 + numpy.exp(-z))

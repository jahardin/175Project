import csv
import random
import os
import re, math, collections, itertools
import nltk
import pickle
import nbHand
import interface
from scipy.io import loadmat
from scipy.sparse import *
import numpy

POS_FILE = 'combinedPos'
NEG_FILE = 'combinedNeg'



class Model():
    def trainNaiveBayes(self):
        numbers_to_test = [10, 100, 1000, 10000, 15000]
        #numbers_to_test = [10]
        try:
            os.remove("statsRecordNB.txt")
        except OSError:
            pass
        
        
    def recordStats(self):
        if(os.path.isfile("statsRecordNB.txt")):
			statsRecord = open("statsRecordNB.txt", "ab") #append
        else:
            statsRecord = open("statsRecordNB.txt", "wb") #write
        
        #load sets
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr']
        
        Yte = loadmat('test.mat')['YTe']
        Xte = loadmat('test.mat')['XTe']
        
        correct = 0
        #training performance
        for i in range(12500, numpy.shape(Xtr)[0]):
            
            x = numpy.zeros([1416, 1])
            
            if(i%10) == 0 and i != 0:
                print "correct: ", correct
                print "i: ", i
            x = numpy.transpose(Xtr[i,:].todense())
            yhat = self.singleClassify(x)
            if(yhat ==  Ytr[i]):
                correct += 1
                
        trainAcc = correct / numpy.shape(Xtr)[0]
        print "trainAcc: ", trainAcc
        
        '''
        string = 'evaluating best %d features\n' % num
        string += 'train on %d instances, test on %d instances(using handwritten algorithm)\n' % (len(trainFeatures), len(testFeatures))
        accuracy = nltk.classify.util.accuracy(classifier, testFeatures)
        string += 'accuracy: %f\n' % accuracy
        posprec = nltk.metrics.precision(referenceSets['pos'], testSets['pos'])
        string += 'pos precision: %f\n' % posprec
        posrecall = nltk.metrics.precision(referenceSets['pos'], testSets['pos'])
        string += 'pos recall: %f\n' % posrecall
        negprec = nltk.metrics.precision(referenceSets['neg'], testSets['neg'])
        string += 'neg precision: %f\n' % negprec
        negrecall = nltk.metrics.recall(referenceSets['neg'], testSets['neg'])
        string += 'neg recall: %f\n\n' % negrecall
        statsRecord.write(string)
        
        string2 = 'evaluating best %d features\n' % num
        string2 += 'train on %d instances, test on %d instances(using NLTK algorithm)\n' % (len(trainFeatures), len(testFeatures))
        accuracy2 = nltk.classify.util.accuracy(classifier_nltk, testFeatures)
        string2 += 'accuracy: %f\n' % accuracy
        posprec2 = nltk.metrics.precision(referenceSets_nltk['pos'], testSets_nltk['pos'])
        string2 += 'pos precision: %f\n' % posprec
        posrecall2 = nltk.metrics.precision(referenceSets_nltk['pos'], testSets_nltk['pos'])
        string2 += 'pos recall: %f\n' % posrecall
        negprec2 = nltk.metrics.precision(referenceSets_nltk['neg'], testSets_nltk['neg'])
        string2 += 'neg precision: %f\n' % negprec
        negrecall2 = nltk.metrics.recall(referenceSets_nltk['neg'], testSets_nltk['neg'])
        string2 += 'neg recall: %f\n\n' % negrecall
        statsRecord.write(string2)
        statsRecord.close()
        print "finished NB features(%d)" % num
        '''
    def evaluate_features(self, feature_select, num):
        posFeatures=[]
        negFeatures=[]
        with open(POS_FILE, 'r') as posSentences:
            for i in posSentences:
                posWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                posWords = [feature_select(posWords), 'pos']
                posFeatures.append(posWords)
        with open(NEG_FILE, 'r') as negSentences:
            for i in negSentences:
                negWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                negWords = [feature_select(negWords), 'neg']
                negFeatures.append(negWords)
                
        ######
        #CLASSIFIER
        ######
        #train the Classifiers
        #print trainFeatures
        
        #train an nltk classifier and non-nltk classifier
        #classifier_nltk = NaiveBayesClassifier.train(trainFeatures)
        
        #save classifiers for later
       
        
        #ff = open('nbclassifier_nltk.pickle', 'wb')
        #pickle.dump(classifier_nltk, ff)
        #ff.close()
        
        #put correctly labeled sentences in reference, predictively labeled in test sets
        for i, (features, label) in enumerate(testFeatures):
            predicted = classifier.classify(features)
         
        self.recordStats()
    #end evaluate_features(feature_select)
    
    def train(self):
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr']
        
        self.cond_prob_pos = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==1),:],2) / numpy.sum(Ytr))
        self.cond_prob_neg = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==0),:],2) / numpy.sum(Ytr==0))
        
        

    
    def singleClassify(self, featureVec):
        #print "singclass shape pos: " , numpy.shape(self.cond_prob_pos)
        #print "singclass shape neg: " , numpy.shape(self.cond_prob_neg)
        neg = numpy.sum(numpy.log(numpy.multiply(featureVec, self.cond_prob_neg) + numpy.multiply(1-featureVec, 1-self.cond_prob_neg)))
        pos = numpy.sum(numpy.log(numpy.multiply(featureVec, self.cond_prob_pos) + numpy.multiply(1-featureVec, 1-self.cond_prob_pos)))
        print "sg pos: ", pos
        print "sg neg: ", neg
        return pos > neg

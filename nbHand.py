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

#####################################
##A handwritten naive bayes implementation
#####################################

class Model():
    def crappyAnalyze(self, features):
        self.train()
        self.singleClassify(features)
	
    def recordStats(self):
        #load sets
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr']
        
        Yte = loadmat('test.mat')['YTe']
        Xte = loadmat('test.mat')['XTe']
        
        correct = 0
        #training performance
        for i in range(12500, numpy.shape(Xtr)[0]):
            x = numpy.zeros([1416, 1])
            if(i%100) == 0 and i != 0:
                print "correct: ", correct
                print "i: ", i
            x = numpy.transpose(Xtr[i,:].todense())
            yhat = self.singleClassify(x) #call to classify
            if(yhat ==  Ytr[i]):
                correct += 1
        trainAcc = float(correct) / float(numpy.shape(Xtr)[0])
        print "trainAcc: ", trainAcc
        
        statsRecord = open("statsRecordNBHand.txt", "w+") #overwrite
        statsRecord.write('train on 18750 instances, test on 6250 instances\n')
        string = 'accuracy %f' % trainAcc
        statsRecord.write(string)
        
        
        
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
    
    def train(self):
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr'] 
        self.cond_prob_pos = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==1),:],2) / numpy.sum(Ytr))
        self.cond_prob_neg = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==0),:],2) / numpy.sum(Ytr==0))
        self.recordStats()
        
    def singleClassify(self, featureVec):
        #print "in single classify"
        neg = numpy.sum(numpy.log(numpy.multiply(featureVec, self.cond_prob_neg) + numpy.multiply(1-featureVec, 1-self.cond_prob_neg)))
        pos = numpy.sum(numpy.log(numpy.multiply(featureVec, self.cond_prob_pos) + numpy.multiply(1-featureVec, 1-self.cond_prob_pos)))
        #print "sg pos: ", pos
        #print "sg neg: ", neg
        return pos > neg

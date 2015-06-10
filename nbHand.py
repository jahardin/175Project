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
    def bow_features(self, words):
        f = open('vocabSVM.txt', 'r')
        word_features = f.read().splitlines()
        features = [0.0] * len(word_features)
        for word in words:
            if word in word_features:
                features[word_features.index(word)] = 1.0
        return features
	
    def inputClasify(self, features):
        #self.train()
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr'] 
        self.cond_prob_pos = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==1),:],2) / numpy.sum(Ytr))
        self.cond_prob_neg = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==0),:],2) / numpy.sum(Ytr==0))
        
        feats = self.bow_features(features)
        feats = numpy.asarray(feats)
        #print "feats before trans: ", feats
        feats = feats.reshape([1416, 1])
        feats.transpose()
        #print "feats after trans: ", feats
        return self.singleClassify(feats)
	
    def recordStats(self):
        #load sets
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr']
        
        Yte = loadmat('test.mat')['YTe']
        Xte = loadmat('test.mat')['XTe']
        
        traincorrect = 0
        #training performance
        print 'training'
        for i in range(0, numpy.shape(Xtr)[0]):
            x = numpy.zeros([1416, 1])
            if(i%1000) == 0 and i != 0:
                print "correct: ", traincorrect
                print "i: ", i
            x = numpy.transpose(Xtr[i,:].todense())
            yhat = self.singleClassify(x) #call to classify
           # print "featurevec: ", x
            if(yhat ==  Ytr[i]):
                traincorrect += 1
                
        trainAcc = float(traincorrect) / float(numpy.shape(Xtr)[0])        
                
        totalcorrect = 0
        totalwrong = 0
        truecorrect = 0
        truewrong = 0
        #testing performance
        print 'testing'
        for i in range(0, numpy.shape(Xte)[0]):
            x = numpy.zeros([1416, 1])
            if(i%1000) == 0 and i != 0:
                print "correct: ", totalcorrect
                print "i: ", i
            x = numpy.transpose(Xte[i,:].todense())
            yhat = self.singleClassify(x) #call to classify
           # print "featurevec: ", x
            if(yhat ==  Yte[i]):
                totalcorrect += 1
            else:
                totalwrong += 1
                
            if(yhat == Yte[i] and yhat == 1):
                truecorrect += 1
            elif(yhat != Yte[i] and yhat ==1):
                truewrong += 1
                
       
        testAcc = float(totalcorrect) / float(numpy.shape(Xte)[0])
        recall = float(truecorrect) / float(12500)
        precision = float(truecorrect) / float(truewrong+truecorrect)
        
        print "trainAcc: ", trainAcc
        print 'testAcc: ', testAcc
        print 'precision: ', precision
        print 'recall: ', recall
        
        statsRecord = open("statsRecordNBHand.txt", "w+") #overwrite
        statsRecord.write('train on 18750 instances, test on 6250 instances\n')
        string = 'training accuracy %f\n' % trainAcc
        string += 'testing accuracy %f\n' % testAcc
        string += 'precision %f\n' % precision
        string += 'recall: %f\n' % recall
        statsRecord.write(string)
        
    
    def train(self):
        Ytr = loadmat('train.mat')['YTr']
        Xtr = loadmat('train.mat')['XTr'] 
        self.cond_prob_pos = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==1),:],2) / numpy.sum(Ytr))
        self.cond_prob_neg = numpy.transpose(csc_matrix.sum(Xtr[numpy.squeeze(Ytr==0),:],2) / numpy.sum(Ytr==0))
                
        self.recordStats()
        
    def singleClassify(self, featureVec):
        #print "in single classify"
        #print "featurevec: ", featureVec
        neg = numpy.sum(numpy.log(numpy.multiply(featureVec, self.cond_prob_neg) + numpy.multiply(1-featureVec, 1-self.cond_prob_neg)))
        pos = numpy.sum(numpy.log(numpy.multiply(featureVec, self.cond_prob_pos) + numpy.multiply(1-featureVec, 1-self.cond_prob_pos)))
        print "sg pos: ", pos
        print "sg neg: ", neg
        print pos > neg
        return pos > neg

import csv
import random
import os
import re, math, collections, itertools
import nltk
from nltk.classify import NaiveBayesClassifier
import pickle
import nbHand

DIR_ROOT = '/home/jacobus/Desktop/175Git/175Project'
POS_FILE = os.path.join(DIR_ROOT, 'combinedPos')
NEG_FILE = os.path.join(DIR_ROOT, 'combinedNeg')

class Model():
    def trainNaiveBayes(self):
        numbers_to_test = [10, 100, 1000, 10000, 15000]
        wordScores = self.create_word_scores()
        print 'using all words as features'
        self.evaluate_features(self.make_full_dict)
        for num in numbers_to_test:
            print 'evaluating best %d word features' % (num)
            best_words = self.find_best_words(wordScores, num)
            #print best_words
            self.evaluate_features(self.best_word_features)
            
    def best_word_features(self, words):
        return dict([(word, True) for word in words if word in best_words])
    
    def make_full_dict(self, words):
        return dict([(word, True) for word in words])
    
    def evaluate_features(self, feature_select):
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
    
        #3/4 of features for training, 1/4 for testing
        posCutoff = int(math.floor(len(posFeatures)*3/4))
        negCutoff = int(math.floor(len(negFeatures)*3/4))
        trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
        testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]
        
        ######
        #CLASSIFIER
        ######
        #train the Classifiers
        print "trainfeats"
        #print trainFeatures
        
        #train an nltk classifier and non-nltk classifier
        classifier_nltk = NaiveBayesClassifier.train(trainFeatures)
        classifier = nbHand.nbClassifierHand.train(trainFeatures)
        
        #save classifiers for later
        f = open('nbclassifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()
        
        ff = open('nbclassifier_nltk.pickle', 'wb')
        pickle.dump(classifier_nltk, ff)
        ff.close()
        
        #make reference set and test sets
        referenceSets = collections.defaultdict(set)
        testSets = collections.defaultdict(set)
        
        #put correctly labeled sentences in reference, predictively labeled in test sets
        for i, (features, label) in enumerate(testFeatures):
            referenceSets[label].add(i)
            predicted = classifier.classify(features)
            testSets[predicted].add(i)
        
        #prints metrics to show how well the feature selection did
        print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
        print ' accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
        print 'pos precision:', nltk.metrics.precision(referenceSets['pos'], testSets['pos'])
        print 'pos recall:', nltk.metrics.recall(referenceSets['pos'], testSets['pos'])
        print 'neg precision:', nltk.metrics.precision(referenceSets['neg'], testSets['neg'])
        print 'neg recall:', nltk.metrics.recall(referenceSets['neg'], testSets['neg'])
        classifier.show_most_informative_features(10)
    #end evaluate_features(feature_select)
    
    def create_word_scores(self):
        #make list of pos and neg words
        posWords=[]
        negWords=[]
        with open(POS_FILE, 'r') as posSentences:
            for i in posSentences:
                posWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                posWords.append(posWord)
    	with open(NEG_FILE, 'r') as negSentences:
            for i in negSentences:
                negWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                negWords.append(negWord)
        posWords = list(itertools.chain(*posWords))
        negWords = list(itertools.chain(*negWords))
        
        #build freq dist of all words, then of words with pos/neg labels
        word_fd = nltk.FreqDist()
        cond_word_fd = nltk.ConditionalFreqDist()
        for word in posWords:
            word_fd[word.lower()] += 1
            cond_word_fd['pos'][word.lower()] += 1
        for word in negWords:
            word_fd[word.lower()] += 1
            cond_word_fd['neg'][word.lower()] += 1
        
        #finds num of pos and neg words/total num of words
        pos_word_count = cond_word_fd['pos'].N()
        neg_word_count = cond_word_fd['neg'].N()
        total_word_count = pos_word_count + neg_word_count
        
        #build dict of words based on chi-squared test    
        word_scores = {}
        for word, freq in word_fd.iteritems():
            pos_score = nltk.BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
            neg_score = nltk.BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)    
            word_scores[word] = pos_score + neg_score
            
        return word_scores
    #end create_word_scores(self)
    
    def find_best_words(self, word_scores, number):
        wordScores = self.create_word_scores()
        best_vals = sorted(wordScores.iteritems(), key=lambda (w,s):s, reverse=True)[:number]
        global best_words; 
        best_words = set([w for w, s in best_vals])
        return best_words

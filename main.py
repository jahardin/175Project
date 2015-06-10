from Tkinter import Tk, Text, BOTH, Menu, W, N, E, S, INSERT, END, Toplevel, Message
import re, math, collections, itertools, os
import pickle
from ttk import Frame
import interface
import logicalRegression
import nbHand
import os.path

class mainInterface():
    def main():
        root = Tk()
        interface.createUI(root)
        app = interface.Example(root)
        root.mainloop()  
        
    ##############################
    ##Classifier Trainers(button callbacks)
    ##############################
    def trainNB(self):
        nbModel = nbHand.Model()
        nbModel.train()
        
    def trainDT(self):
        dtModel = decisionTreeModel.Model()
        dtModel.trainDecisionTree()
        
    def trainMultiNB(self):
        multiNBModel = multinomialNBModel.Model()
        multiNBModel.trainMultinomialNB()
        
        '''
    def trainSVC(self):
		vectorModel = svcModel.Model()
		vectorModel.trainSVC()
        '''
    
    ##############################
    ##Classifier Use Functions(button callbacks)
    ##############################
    def analyzeNB(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        m = nbHand.Model()
        posnegbool = m.inputClasify(wordList)
        if(posnegbool == 1):
            posnegword = 'pos'
        else:
            posnegword = 'neg'
            
        posneg.delete(1.0, END)
        posneg.insert(INSERT, posnegword)
        '''
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('nbclassifier.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        '''
        
    def analyzeNB_nltk(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('nbclassifier_nltk.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeSVC(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('svcclassifier_backup.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
        
    def analyzeLogReg(self, area, scorebox2):
        inp = area.get("1.0",'end-1c')
        #self.calc_log_regression(inp)
        l = logicalRegression.Regression()
        test = l.calc_log_regression(inp)
        scorebox2.delete(1.0, END)
        scorebox2.insert(INSERT, test)
    
    def showStats(self, area2):
		if(os.path.exists('statsRecordNB.txt')):
			statsRecordNB = open('statsRecordNB.txt', 'r')
			statsNB = statsRecordNB.read()
			area2.insert(INSERT, "NAIVE BAYES STATISTICS NLTK\n")
			area2.insert(INSERT, statsNB)
			statsRecordNBHand = open('statsRecordNBHand.txt', 'r')
		if(os.path.exists('statsRecordNBHand.txt')):
			statsRecordNB = open('statsRecordNBHand.txt', 'r')
			statsNB = statsRecordNB.read()
			area2.insert(END, "\n\nNAIVE BAYES STATISTICS HAND CLASSIFIER\n")
			area2.insert(END, statsNB)
			statsRecordNBHand = open('statsRecordNBHand.txt', 'r')
		if(os.path.exists('statsRecordSVC.txt')):
			statsRecordNB = open('statsRecordSVC.txt', 'r')
			statsNB = statsRecordNB.read()
			area2.insert(END, statsNB)
			statsRecordNBHand = open('statsRecordSVC.txt', 'r')
      
    ##############################
    ##End Classifier Use Functions
    ##############################




    if __name__ == '__main__':
        main()
